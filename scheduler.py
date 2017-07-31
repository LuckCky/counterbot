#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler

from scheduler_job import get_all_fans_job

# initialize scheduler
SCHEDULER = BackgroundScheduler()
SCHEDULER.start()


class Scheduler(object):

    def __init__(self):
        self.hour = '23.38'

    def add_get_all_fans_job(self):
        SCHEDULER.add_job(get_all_fans_job(), 'cron', hour=self.hour, misfire_grace_time=120)
