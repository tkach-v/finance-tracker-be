import datetime
import os

from celery import Celery
from celery.schedules import crontab

from finance_tracker.settings import CELERY_BROKER_URL

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_tracker.settings")

app = Celery("finance_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.ONCE = {
    "backend": "celery_once.backends.Redis",
    "settings": {
        "url": CELERY_BROKER_URL,
        "default_timeout": datetime.timedelta(minutes=15).total_seconds(),
    },
}

app.conf.beat_schedule = {
    "update-currencies-every-hour": {
        "task": "currencies.tasks.update_currencies",
        "schedule": crontab(minute="*"),  # TODO: change to every hour
        "args": (),
    },
}
