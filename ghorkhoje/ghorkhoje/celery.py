import os

from celery import Celery
from django.conf import settings

import requests
from celery import current_app as app
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ghorkhoje.settings")

app = Celery("ghorkhoje")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Retry connection on startup
app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def health_check(self):
    url = "https://ghor-khoje-backend.onrender.com/health/"
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    print("[{}] Health check task started".format(timestamp))

    try:
        # Make HTTP request with timeout
        response = requests.get(
            url, timeout=30, headers={"User-Agent": "Celery-Health-Check/1.0"}
        )
        print(response.data)
        print(f"[{timestamp}] Health check task completed")
    except Exception as e:
        print(f"[{timestamp}] Health check task failed: {str(e)}")
