from django.http import JsonResponse
from .models import Device, Site

def register_device(request):
    device_id = request.GET.get('device_id')
    site_name = request.GET.get('site_name')
    
    # Find or create site
    site, created = Site.objects.get_or_create(site_name=site_name)
    
    # Register device
    device, created = Device.objects.get_or_create(device_id=device_id, defaults={'site': site})
    
    if created:
        return JsonResponse({"status": "Device registered", "device_id": device_id, "site": site_name})
    else:
        return JsonResponse({"status": "Device already exists", "device_id": device_id, "site": site_name})
