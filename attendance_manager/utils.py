import boto3
from io import BytesIO
from PIL import Image
import os

# def get_image_url(image_key):
#     """
#     Generate the full URL for an image stored in S3 using bucket and folder from .env.
#     """
#     bucket_name = os.getenv('bucket_name')  # Get the bucket name from .env
#     s3_folder = os.getenv('s3_folder')  # Get the folder path from .env
#     return f"https://{bucket_name}.s3.amazonaws.com/{s3_folder}{image_key}"

def get_image_url(image_key):
    """
    Generate a signed URL for accessing an image in the S3 bucket.
    The URL is valid for a limited time.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('aws_access_key'),
        aws_secret_access_key=os.getenv('aws_secret_key'),
        region_name='us-east-1'
    )
    bucket_name = os.getenv('bucket_name')
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': image_key},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        return url
    except Exception as e:
        print(f"Error generating signed URL: {str(e)}")
        return None

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
    
