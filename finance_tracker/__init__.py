from finance_tracker.celery import app
from finance_tracker.celery import app as celery_app

__all__ = ("celery_app", "app")
