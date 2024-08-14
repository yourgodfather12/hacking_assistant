from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def add_scan_job(func, target: str, interval: int) -> None:
    """Add a scan job to the scheduler."""
    try:
        scheduler.add_job(func, 'interval', args=[target], minutes=interval)
        scheduler.start()
        logger.info(f"Scheduled scan job for target {target} every {interval} minutes.")
    except Exception as e:
        logger.error(f"Error scheduling scan job for target {target}: {e}")
