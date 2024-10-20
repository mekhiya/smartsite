from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_tracker_project.settings')

app = Celery('smart_tracker_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Optional task to check Celery functionality
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
