from django.http import JsonResponse
from .tasks import process_attendance

def handle_attendance(request):
    image_key = request.GET.get('image_key')
    bucket_name = request.GET.get('bucket_name')
    device_id = request.GET.get('device_id')
    site_id = request.GET.get('site_id')

    # Trigger the asynchronous task
    task = process_attendance.delay(image_key, bucket_name, device_id, site_id)
    
    return JsonResponse({'status': 'success', 'task_id': task.id})
