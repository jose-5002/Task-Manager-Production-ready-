import os
from celery import Celery

#Celery wiring into the project

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
app = Celery('Backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()