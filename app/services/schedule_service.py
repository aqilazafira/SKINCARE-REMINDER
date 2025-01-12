from typing import Callable

from app import scheduler

def create_schedule(action: Callable, hour, minute):
    job = scheduler.add_job(
        action, "cron", hour=hour, minute=minute
    )
    print(f"creating schedule {hour}: {minute} {job}")
    return job.id

def delete_schedule(job_id):
    scheduler.remove_job(job_id)
    print("Schedule removed")

def reschedule(id: str, hour: int, minute: int):
    scheduler.reschedule_job(id, "cron", hour=hour, minute=minute)
