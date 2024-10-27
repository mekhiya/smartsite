import logging
import pickle
import io, os
import face_recognition
import boto3
from attendance_manager.models import Person
from celery import shared_task

# Set up logging
logger = logging.getLogger(__name__)

# Initialize S3 client with environment variables
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('aws_access_key'),
    aws_secret_access_key=os.getenv('aws_secret_key'),
    region_name=os.getenv('aws_region')
)

@shared_task
def process_attendance(image_key, bucket_name, device_id, site_id):
    # Log AWS credentials to confirm they are loaded (for debugging)
    logger.info(f"AWS Access Key: {os.getenv('aws_access_key')}")
    logger.info(f"AWS Secret Key: {os.getenv('aws_secret_key')}")

    try:
        # Log start of attendance processing
        logger.info(f"Starting attendance processing for image_key={image_key}, bucket_name={bucket_name}, device_id={device_id}, site_id={site_id}")

        # Step 1: Download the image from S3
        response = s3.get_object(Bucket=bucket_name, Key=image_key)
        image_data = response['Body'].read()
        logger.info(f"Successfully downloaded image {image_key} from S3")

        # Step 2: Load image with face_recognition using io.BytesIO
        image = face_recognition.load_image_file(io.BytesIO(image_data))
        encodings = face_recognition.face_encodings(image)

        # Check if faces are detected
        if encodings:
            logger.info(f"Number of faces detected: {len(encodings)}")
            encoding = encodings[0]

            # Step 3: Compare with existing encodings in the database
            for person in Person.objects.all():
                person_encoding = pickle.loads(person.face_encoding)
                matches = face_recognition.compare_faces([person_encoding], encoding, tolerance=0.6)
                if True in matches:
                    logger.info(f"Attendance recorded for {person.name}")
                    # Add any logic needed to update or save attendance data in the database here
                    return {
                        "status": "success",
                        "person": person.name,
                        "site_id": site_id,
                        "device_id": device_id,
                    }
            logger.info("No matching face found in the database")
            return {"status": "unmatched", "message": "No matching face found"}

        else:
            logger.info("No face detected in the image")
            return {"status": "error", "message": "No face detected"}

    except Exception as e:
        # Log any exception that occurs during processing
        logger.error(f"Error processing attendance for image {image_key}: {e}")
        return {"status": "error", "message": str(e)}
