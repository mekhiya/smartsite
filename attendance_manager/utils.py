import boto3
from io import BytesIO
from PIL import Image
import os

class S3ImageHandler:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('aws_access_key'),  # Use os.getenv here
            aws_secret_access_key=os.getenv('aws_secret_key'),  # Use os.getenv here
            region_name='us-east-1'
        )

    def download_image(self, bucket_name, image_key):
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=image_key)
            image_data = response['Body'].read()
            image = Image.open(BytesIO(image_data))
            return image
        except Exception as e:
            print(f"Error downloading image from S3: {str(e)}")
            return None
