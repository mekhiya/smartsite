celery -A smart_tracker_project worker --loglevel=info

celery -A smart_tracker_project beat --loglevel=info

export $(grep -v '^#' .env | xargs)

<!-- toverify if export worked inside shell -->
python manage.py shell

import os
print(os.getenv('aws_access_key'))
print(os.getenv('aws_secret_key'))
print(os.getenv('aws_region'))
print(os.getenv('bucket_name'))
print(os.getenv('s3_folder'))


celery -A smart_tracker_project worker --loglevel=info


curl "http://localhost:8000/test_app/add_sync/?a=2&b=3"

curl "http://localhost:8000/test_app/add_async/?a=2&b=3"

curl "http://localhost:8000/test_app/check_task_status/?task_id=fa9f7aa3-7af9-40d1-8691-bc2d4fc5be06"


curl "http://localhost:8000/device_registration/register_device/?device_id=unique_device_id_123&site_name=site_001"



curl "http://localhost:8000/attendance_manager/handle_attendance/?image_key=siteimages/IMG_20240331_131148.jpg&bucket_name=sitemonitors3&device_id=unique_device_id_123&site_id=site_001"


curl "http://localhost:8000/attendance_manager/handle_attendance/?image_key=siteimages/sachin-5.png&bucket_name=sitemonitors3&device_id=unique_device_id_123&site_id=site_001"




