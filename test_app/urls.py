from django.urls import path
from test_app import views

urlpatterns = [
    path('add_sync/', views.add_sync,name='add_sync'),
    path('add_async/', views.add_async, name='add_async'),
    path('check_task_status/', views.check_task_status, name='check_task_status'),
]