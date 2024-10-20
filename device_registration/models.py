from django.db import models

class Site(models.Model):
    site_name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)
