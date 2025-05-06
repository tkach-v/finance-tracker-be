from celery_once import QueueOnce

from finance_tracker.celery import app
from finance_tracker.scripts.update_active_currencies import update_active_currencies


@app.task(base=QueueOnce, once={"graceful": True})
def update_currencies():
    """
    Update the current price of every active currency in the database (in a Currency model).
    Also save the current price with data in the database (in a CurrencyPrice model).
    """
    update_active_currencies()
