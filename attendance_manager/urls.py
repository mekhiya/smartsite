from django.urls import path
from . import views

urlpatterns = [
    path('handle_attendance/', views.handle_attendance, name='handle_attendance'),
]
