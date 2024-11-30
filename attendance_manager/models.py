from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default='Unknown')
    face_encoding = models.BinaryField()

    def __str__(self):
        return self.name


class AttendanceRecord(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    # unregistered_face = models.ForeignKey('UnregisteredFaces', on_delete=models.CASCADE, null=True, blank=True)
    unregistered_face = models.ForeignKey('UnregisteredFaces', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='attendance_images/')
    status = models.CharField(max_length=50)  # e.g., Present, Absent, etc.


class UnregisteredFaces(models.Model):
    image_key = models.CharField(max_length=255)
    face_encoding = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
    occurrences = models.IntegerField(default=1)
    quality_score = models.FloatField(default=0.0)  # Placeholder for quality score
    device_id = models.CharField(max_length=255)
    site_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Unregistered Face from {self.device_id} at {self.timestamp}"
