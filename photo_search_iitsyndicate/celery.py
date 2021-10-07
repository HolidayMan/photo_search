from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_search_iitsyndicate.settings')

app = Celery('photo_search_iitsyndicate')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
