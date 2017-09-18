#!/usr/bin/env python3

import os

import telebot

from utils.utils import get_project_names_list, get_all_fans_count

token = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(token)


def get_all_fans_job():
    print("!!!!!!!!11 scheduler started!!!!!!!")
    project_names_list = get_project_names_list()
    result = get_all_fans_count(project_names_list)
    for message in result:
        bot.send_message(CHAT_ID, message)
