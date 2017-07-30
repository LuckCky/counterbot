#!/usr/bin/env python3

import os
import time

import cherrypy
import telebot

import conf
from scheduler import Scheduler
import utils.fill_db
from utils.utils import message_parser, report_needed, get_resource_name_from_alias, get_fans_count
from utils.utils import get_project_names_list, get_all_fans_count, get_report_size
from utils.db_works import DBWorks

token = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

WEBHOOK_PORT = int(os.environ.get('PORT', '5000'))
WEBHOOK_LISTEN = conf.webhook_listen

WEBHOOK_URL_BASE = conf.post_url
WEBHOOK_URL_PATH = "/{}/".format(token)

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def get_fans(message):
    print(message.chat.id)
    report_size = get_report_size(message.text)
    if report_size == "big":
        project_names_list = get_project_names_list()
        result = get_all_fans_count(project_names_list)
        for message_text in result:
            bot.send_message(message.chat.id, message_text)
        return
    if report_needed(message.text):
        alias, network = message_parser(message.text)
    else:
        return
    if not alias:
        bot.send_message(message.chat.id, "Забыли указать ресурс:(")
        return
    resource_name = get_resource_name_from_alias(alias)
    if not resource_name:
        bot.send_message(message.chat.id, "Неверный алиас для ресурса, попробуйте снова")
        return
    number_of_fans, error_text, _network = get_fans_count(resource_name, network)
    if error_text:
        bot.send_message(message.chat.id, "Тут ошибки возникли для проекта '{}' в '{}', "
                                          "вот текст: '{}', "
                                          "но я постараюсь по остальным соцсетям посчитать подписчиков"
                         .format(resource_name, _network, error_text))
    if not network:
        message_to_send = "У ресурса {} количество подписчиков {}".format(resource_name, number_of_fans)
    else:
        message_to_send = "У ресурса {} количество подписчиков {} в {}".format(resource_name, number_of_fans, network)
    bot.send_message(message.chat.id, message_to_send)
    return


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


if __name__ == "__main__":
    DBWorks().fire_up_db()
    utils.fill_db.main()
    Scheduler().add_get_all_fans_job()
    bot.remove_webhook()
    time.sleep(3)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

    cherrypy.config.update({
        'engine.autoreload.on': False,
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
    })

    # RUN SERVER, RUN!
    cherrypy.tree.mount(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

    cherrypy.engine.start()
    cherrypy.engine.block()
    # bot.polling()
