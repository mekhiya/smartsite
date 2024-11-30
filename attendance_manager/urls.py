from django.urls import path
from . import views

urlpatterns = [
    path('unregistered_faces/', views.view_unregistered_faces, name='view_unregistered_faces'),
    path('register_person/', views.register_person, name='register_person'),
    path('handle_attendance/', views.handle_attendance, name='handle_attendance'),  # Add this line
]
