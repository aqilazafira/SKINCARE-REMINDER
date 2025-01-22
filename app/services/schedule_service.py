from flask import current_app
from typing import Callable

from app import scheduler

def create_schedule(action: Callable, day: int, hour: int, minute: int):
    job = scheduler.add_job(
        action, "cron", day_of_week=day, hour=hour, minute=minute
    )
    current_app.logger.info(f"creating schedule for {day} - {hour}:{minute}, id={job}")
    return job.id

def delete_schedule(job_id):
    scheduler.remove_job(job_id)
    print("Schedule removed")

def reschedule(id: str, day: int, hour: int, minute: int):
    scheduler.reschedule_job(id, "cron", day_of_week=day, hour=hour, minute=minute)
