from django.shortcuts import render
from django.http import JsonResponse
from .tasks import add
from celery.result import AsyncResult  # Add this import


# Create your views here.
def add_sync(request):
    a   = int(request.GET.get('a'))
    b = int(request.GET.get('b'))
    result=a+b
    return JsonResponse({'sum': result})

def add_async(request):
    a = int(request.GET.get('a'))
    b = int(request.GET.get('b'))
    
    # Use Celery to process the task asynchronously
    task = add.delay(a, b)  # `delay` is used to call the Celery task asynchronously
    
    # Respond with task ID for the user to track the status
    return JsonResponse({'status': 'success', 'task_id': task.id})


def check_task_status(request):
    task_id = request.GET.get('task_id')
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        response = {'status': 'Pending...'}
    elif task_result.state == 'SUCCESS':
        response = {'status': 'Completed', 'result': task_result.result}
    else:
        response = {'status': task_result.state}
    
    return JsonResponse(response)
