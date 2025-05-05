from celery_once import QueueOnce

from finance_tracker.celery import app


@app.task(base=QueueOnce, once={"graceful": True})
def update_currencies():
    """
    Update the current price of every active currency in the database (in a Currency model).
    Also save the current price with data in the database (in a CurrencyPrice model).
    """
    print("Updating currencies...")
