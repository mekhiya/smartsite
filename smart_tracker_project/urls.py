from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_app/', include('test_app.urls')),
    path('device_registration/', include('device_registration.urls')),
    path('attendance_manager/', include('attendance_manager.urls')),  # Ensure this line exists
]
