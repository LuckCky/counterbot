#!/usr/bin/env python3

from apscheduler.schedulers.background import BlockingScheduler

from scheduler_job import get_all_fans_job

# initialize scheduler
SCHEDULER = BlockingScheduler()
SCHEDULER.start()


class Scheduler(object):

    def __init__(self):
        self.hour = 20

    def add_get_all_fans_job(self):
        SCHEDULER.add_job(get_all_fans_job(), 'cron', hour=self.hour)

if __name__ == "__main__":
    s = Scheduler()
    s.add_get_all_fans_job()
