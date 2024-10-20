from celery import shared_task
from .models import Person, AttendanceRecord
from .utils import S3ImageHandler
import face_recognition
import numpy as np

@shared_task
def process_attendance(image_key, bucket_name, device_id, site_id):
    # Initialize the S3 Image Handler
    image_handler = S3ImageHandler()

    # Download the image from S3
    image = image_handler.download_image(bucket_name, image_key)
    if not image:
        return {"status": "error", "message": "Image download failed"}

    # Convert image to RGB if not already in that format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert the image object to a numpy array
    image_array = np.array(image)

    # Find face locations and encodings
    face_locations = face_recognition.face_locations(image_array)
    face_encodings = face_recognition.face_encodings(image_array, face_locations)

    if len(face_encodings) == 0:
        return {"status": "error", "message": "No face detected"}

    matched_person = None
    for encoding in face_encodings:
        # Compare each face encoding with known persons in the system
        people = Person.objects.all()
        for person in people:
            matches = face_recognition.compare_faces([person.face_encoding], encoding)
            if True in matches:
                matched_person = person
                break

    if matched_person:
        # Create a new attendance record
        AttendanceRecord.objects.create(person=matched_person, status="Present", image=image_key, site_id=site_id, device_id=device_id)
        return {"status": "success", "person": matched_person.name, "site_id": site_id, "device_id": device_id}
    else:
        return {"status": "unmatched", "message": "No matching face found"}
