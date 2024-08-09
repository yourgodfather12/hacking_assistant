from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def add_scan_job(func, target, interval):
    scheduler.add_job(func, 'interval', args=[target], minutes=interval)
    scheduler.start()
