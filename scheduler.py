import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def daily_job():
    logging.info("Daily scheduled job executed at 11:59 PM.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=23, minute=59)
    scheduler.add_job(daily_job, trigger, id="daily_job", replace_existing=True)
    scheduler.start()
    logging.info("Scheduler started: daily job scheduled for 11:59 PM.")
