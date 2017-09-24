#!/usr/bin/env python3

# from scheduler import Scheduler
#
# s = Scheduler()
# s.add_get_all_fans_job()
# print("I started!!!!!!!")

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
