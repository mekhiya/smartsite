from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    face_encoding = models.BinaryField()

class AttendanceRecord(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='attendance_images/')
    status = models.CharField(max_length=50)  # e.g., Present, Absent, etc.
