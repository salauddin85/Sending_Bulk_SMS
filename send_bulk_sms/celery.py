from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'send_bulk_sms.settings')

app = Celery('send_bulk_sms')
app.conf.update(timezone='Asia/Dhaka')
app.config_from_object(settings, namespace='CELERY')

# For Autodiscover tasks
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
