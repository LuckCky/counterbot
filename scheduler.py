#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler

from logger import init_logger
from scheduler_job import Job

scheduler_logger = init_logger('scheduler logger')

# initialize scheduler
SCHEDULER = BackgroundScheduler()
SCHEDULER.start()
scheduler_logger.info('SCHEDULER started')


class Scheduler(object):

    def __init__(self):
        self.hour = 12
        self.job = Job()
        scheduler_logger.info('SCHEDULER initialized to run at {}'.format(self.hour))

    def add_get_all_fans_job(self):
        SCHEDULER.add_job(self.job.get_all_fans_job, 'cron', hour=self.hour, minute=00)
        scheduler_logger.info('adding job to fire at: {}'.format(self.hour))


if __name__ == '__main__':
    Scheduler().add_get_all_fans_job()
