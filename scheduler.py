#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler

from scheduler_job import get_all_fans_job

# initialize scheduler
SCHEDULER = BackgroundScheduler()
SCHEDULER.start()


class Scheduler(object):

    def __init__(self):
        self.hour = '22.00'
        self.hour1 = '23.00'
        self.hour2 = '00.00'

    def add_get_all_fans_job(self):
        SCHEDULER.add_job(get_all_fans_job(), 'cron', hour=self.hour)#, misfire_grace_time=120)

    def add_get_all_fans_job1(self):
        SCHEDULER.add_job(get_all_fans_job(), 'cron', hour=self.hour1)

    def add_get_all_fans_job2(self):
        SCHEDULER.add_job(get_all_fans_job(), 'cron', hour=self.hour2)

if __name__ == "__main__":
    s = Scheduler()
    s.add_get_all_fans_job()
    s.add_get_all_fans_job1()
    s.add_get_all_fans_job2()
