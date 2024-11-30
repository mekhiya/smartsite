from datetime import datetime
import logging
import face_recognition
import numpy as np
from celery import shared_task
from django.utils.timezone import now
from attendance_manager.models import Person, AttendanceRecord, UnregisteredFaces
from .utils import S3ImageHandler

logger = logging.getLogger(__name__)

# Thresholds for face matching
THRESHOLD_MATCH = 0.4  # Strict threshold for registered matches
THRESHOLD_POSSIBLE_NEW = 0.5  # Secondary threshold for potential new unregistered faces

def process_face(encoding, all_persons, all_unregistered_faces, image_key, device_id, site_id):
    """
    Process a single face encoding: Match it with registered persons or unregistered faces,
    or create a new unregistered face entry.
    """
    closest_distance = float('inf')
    best_match = None

    # Compare with registered persons
    for person in all_persons:
        stored_encoding = np.frombuffer(person.face_encoding, dtype=np.float64)
        distance = np.linalg.norm(stored_encoding - encoding)
        if distance < closest_distance:
            closest_distance = distance
            best_match = person

    # If match is below strict threshold, assign to existing person
    if closest_distance < THRESHOLD_MATCH:
        # Update the person's encoding to improve quality
        person_encoding = np.frombuffer(best_match.face_encoding, dtype=np.float64)
        new_encoding = np.mean([person_encoding, encoding], axis=0)
        
        # best_match.face_encoding = new_encoding.tobytes()
        # best_match.save()
        
        # Save only if the encoding actually changes
        if not np.array_equal(person_encoding, new_encoding):
            best_match.face_encoding = new_encoding.tobytes()
            best_match.save()

        AttendanceRecord.objects.create(
            person=best_match,
            timestamp=now(),
            image=image_key,
            status="Present"
        )
        logger.info(f"Matched with registered person: {best_match.name}")
        return f"Matched with registered person: {best_match.name}"

    # Compare with unregistered faces
    closest_distance = float('inf')
    best_match = None
    for unregistered_face in all_unregistered_faces:
        stored_encoding = np.frombuffer(unregistered_face.face_encoding, dtype=np.float64)
        distance = np.linalg.norm(stored_encoding - encoding)
        if distance < closest_distance:
            closest_distance = distance
            best_match = unregistered_face

    # If match is below secondary threshold, use existing unregistered face
    if closest_distance < THRESHOLD_POSSIBLE_NEW:
        best_match.occurrences += 1
        best_match.timestamp = now()
        best_match.save()

        AttendanceRecord.objects.create(
            unregistered_face=best_match,
            timestamp=now(),
            image=image_key,
            status="Unregistered"
        )
        logger.info(f"Matched with existing unregistered face: {best_match.id}")
        return f"Matched with existing unregistered face: {best_match.id}"

    # Otherwise, create a new unregistered face
    new_unregistered_face = UnregisteredFaces.objects.create(
        image_key=image_key,
        face_encoding=encoding.tobytes(),
        timestamp=now(),
        device_id=device_id,
        site_id=site_id
    )

    AttendanceRecord.objects.create(
        unregistered_face=new_unregistered_face,
        timestamp=now(),
        image=image_key,
        status="Unregistered"
    )
    logger.info(f"Created new unregistered face: {new_unregistered_face.id}")
    return f"Created new unregistered face: {new_unregistered_face.id}"

@shared_task
def process_attendance(image_key, bucket_name, device_id, site_id):
    """
    Process attendance for a given image by detecting faces and matching them to
    registered persons or unregistered faces.
    """
    try:
        # Step 1: Download image from S3
        image_handler = S3ImageHandler()
        image = image_handler.download_image(bucket_name, image_key)
        if image is None:
            logger.error("Failed to download image from S3.")
            return

        # Convert PIL image to RGB if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert PIL image to a format that face_recognition can handle
        image_array = np.array(image)

        logger.info(f"Processing image {image_key} for attendance.")

        # Step 2: Detect and encode face(s) from the image
        face_encodings = face_recognition.face_encodings(image_array)
        logger.info(f"Number of faces detected: {len(face_encodings)}")

        if not face_encodings:
            logger.warning("No faces detected in the image.")
            return

        # Get all persons and unregistered faces from the database
        all_persons = Person.objects.all()
        all_unregistered_faces = UnregisteredFaces.objects.all()

        # Step 3: Process each face encoding
        for encoding in face_encodings:
            result = process_face(encoding, all_persons, all_unregistered_faces, image_key, device_id, site_id)
            logger.info(result)

    except Exception as e:
        logger.error(f"Error processing attendance: {e}")
