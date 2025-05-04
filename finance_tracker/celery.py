import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_tracker.settings")

app = Celery("finance_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {}
