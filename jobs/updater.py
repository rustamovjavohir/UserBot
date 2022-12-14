from apscheduler.schedulers.background import BackgroundScheduler

from jobs.jobs import updateTotal


def startUpdater():
    sss = BackgroundScheduler({'apscheduler.timezone': 'Asia/Tashkent'})
    sss.add_job(updateTotal, "interval", seconds=300)
    sss.add_job(updateTotal, "cron", hour=13, minute=21)
    # sss.add_job(salary, "cron", hour=11, minute=42)
    # sss.add_job(ttime, "cron", hour=23, minute=50)
    # sss.add_job(hero_month, "cron", month="1-12", day=1, hour=5, minute=30)
    sss.start()
