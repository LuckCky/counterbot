#!/usr/bin/env python3

import os
import time

import cherrypy
import telebot

import conf
import utils.fill_db

from utils.utils import message_parser, report_needed, get_resource_name_from_alias
from utils.db_works import DBWorks

token = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

WEBHOOK_PORT = int(os.environ.get('PORT', '5000'))
WEBHOOK_LISTEN = conf.webhook_listen

WEBHOOK_URL_BASE = conf.post_url
WEBHOOK_URL_PATH = "/{}/".format(token)

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
                                    'voice', 'location', 'contact'])
def get_fans(message):
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
    number_of_fans = get_fans(resource_name, network)
    if not network:
        message_to_send = "У ресурса {} количество подписчиков {}".format(resource_name, number_of_fans)
    else:
        message_to_send = "У ресурса {} количество подписчиков {} в {}".format(resource_name, number_of_fans, network)
    bot.send_message(message.chat.id, message_to_send)


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
