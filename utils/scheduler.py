"""
Background scheduler for practice reminders.
In a Streamlit app, this runs as a lightweight in-process scheduler.
For production, move this to a standalone FastAPI worker.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

_scheduler = BackgroundScheduler()
_started = False


def _check_reminders():
    """Placeholder: in production, query DB and send email/push reminders."""
    print(f"[{datetime.now()}] Checking practice reminders...")


def start_scheduler():
    global _started
    if not _started:
        _scheduler.add_job(_check_reminders, "interval", hours=24, id="reminders")
        _scheduler.start()
        _started = True


def stop_scheduler():
    if _started:
        _scheduler.shutdown(wait=False)
