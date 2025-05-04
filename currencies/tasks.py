from celery_once import QueueOnce

from finance_tracker.celery import app


@app.task(base=QueueOnce, once={"graceful": True})
def update_currencies():
    print("Updating currencies...")
