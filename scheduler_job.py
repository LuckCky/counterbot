#!/usr/bin/env python3

import os

import telebot

from logger import init_logger
from utils.utils import get_project_names_list, get_all_fans_count
from set_vars import set_vars
set_vars()

jobs_logger = init_logger('jobs logger')

token = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
jobs_logger.info('envinron variables received')

bot = telebot.TeleBot(token)


class Job(object):
    @staticmethod
    def get_all_fans_job():
        jobs_logger.info("job started")
        project_names_list = get_project_names_list()
        result = get_all_fans_count(project_names_list)
        # result = ['Сейчас', '12 часов', 'дня']
        for message in result:
            bot.send_message(CHAT_ID, message)
        jobs_logger.info("job done")


if __name__ == '__main__':
    Job.get_all_fans_job()
