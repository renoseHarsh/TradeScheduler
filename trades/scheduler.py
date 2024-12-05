# trades/scheduler.py
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


# Define the job function to print the current time
def print_time():
    now = datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_time, "interval", seconds=10)
    scheduler.start()
