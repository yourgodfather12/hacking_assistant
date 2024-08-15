from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def add_scan_job(func, target: str, interval: int) -> None:
    """Add a scan job to the scheduler."""
    try:
        job = scheduler.add_job(func, 'interval', args=[target], minutes=interval)
        scheduler.start()
        logger.info(f"Scheduled scan job for target {target} every {interval} minutes.")
    except Exception as e:
        logger.error(f"Error scheduling scan job for target {target}: {e}")

def list_jobs():
    """List all scheduled jobs."""
    jobs = scheduler.get_jobs()
    for job in jobs:
        logger.info(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}")

def pause_job(job_id: str):
    """Pause a specific job."""
    try:
        scheduler.pause_job(job_id)
        logger.info(f"Job {job_id} paused.")
    except Exception as e:
        logger.error(f"Error pausing job {job_id}: {e}")

def resume_job(job_id: str):
    """Resume a specific job."""
    try:
        scheduler.resume_job(job_id)
        logger.info(f"Job {job_id} resumed.")
    except Exception as e:
        logger.error(f"Error resuming job {job_id}: {e}")

def remove_job(job_id: str):
    """Remove a specific job."""
    try:
        scheduler.remove_job(job_id)
        logger.info(f"Job {job_id} removed.")
    except Exception as e:
        logger.error(f"Error removing job {job_id}: {e}")
