#!/usr/bin/env python3

import os
import time

import cherrypy
import telebot

import conf
from logger import init_logger
from scheduler import Scheduler
from set_vars import set_vars
set_vars()
import utils.fill_db
from utils.utils import message_parser, report_needed, get_resource_name_from_alias, get_fans_count
from utils.utils import get_project_names_list, get_all_fans_count, get_report_size
from utils.db_works import DBWorks

bot_log = init_logger('bot logger')

token = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# WEBHOOK_PORT = int(os.environ.get('PORT', '5000'))
# WEBHOOK_LISTEN = conf.webhook_listen

# WEBHOOK_URL_BASE = conf.post_url
# WEBHOOK_URL_PATH = "/{}/".format(token)

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def get_fans(message):
    bot_log.info('message received: {} from chat {}'.format(message.text, message.chat.id))
    # if message.text == "бот, заряжай":
    #     bot.send_message(message.chat.id, "Готовлюсь")
    #     bot_log.info('preparing to start scheduler')
    #     s = Scheduler()
    #     bot_log.info('scheduler instance created')
    #     bot_log.info('preparing to add job')
    #     s.add_get_all_fans_job()
    #     bot_log.info('job added')
    #     bot.send_message(message.chat.id, "А готово!")
    #     return
    report_size = get_report_size(message.text)
    bot_log.info('defined report size:', report_size)
    if report_size == "big":
        project_names_list = get_project_names_list()
        bot_log.info('defined projects names list: {}'.format(str(project_names_list)))
        result = get_all_fans_count(project_names_list)
        bot_log.info('got results for all projects')
        for message_text in result:
            bot_log.info('result for every project: {}'.format(str(message_text)))
            bot.send_message(message.chat.id, message_text)
            bot_log.info('all messages for results are sent')
        return
    if report_needed(message.text):
        alias, network = message_parser(message.text)
        bot_log.info('report needed for alias ({}) and network ({})'.format(alias, network))
    else:
        bot_log.info('report not needed')
        return
    if not alias:
        bot_log.info('no alias provided')
        bot.send_message(message.chat.id, "Забыли указать ресурс:(")
        return
    resource_name = get_resource_name_from_alias(alias)
    if not resource_name:
        bot_log.info('no resource name found for alias {}'.format(alias))
        bot.send_message(message.chat.id, "Неверный алиас для ресурса, попробуйте снова")
        return
    number_of_fans, error_text, _network = get_fans_count(resource_name, network)
    bot_log.info('got number of fans, error text and network')
    if error_text:
        bot_log.info('got error text for ({)). It is {}'.format(_network, error_text))
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
    bot_log.info('starting to prepare DB')
    DBWorks().fire_up_db()
    bot_log.info('db fired up')
    bot_log.info('preparing to fill db with data')
    utils.fill_db.main()
    bot_log.info('db prepared')
    bot_log.info('removing webhook')
    bot.remove_webhook()
    bot_log.info('webhook removed')
    bot_log.info('starting scheduler')
    # Scheduler().add_get_all_fans_job()
    # time.sleep(3)
    # bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    #
    # cherrypy.config.update({
    #     'engine.autoreload.on': False,
    #     'server.socket_host': WEBHOOK_LISTEN,
    #     'server.socket_port': WEBHOOK_PORT,
    # })
    #
    # RUN SERVER, RUN!
    # cherrypy.tree.mount(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
    #
    # cherrypy.engine.start()
    # cherrypy.engine.block()
    # print('starting bot')
    bot.polling(none_stop=True)
