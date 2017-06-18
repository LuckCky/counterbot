#!/usr/bin/env python3

import os
import time

import cherrypy
import telebot

import conf
from social_stuff.fb import get_fb_fans
from social_stuff.ok import get_ok_fans
from social_stuff.twi import get_twi_fans
from social_stuff.vk_info import get_vk_fans
from social_stuff.youtube import get_youtube_fans
from utils.utils import message_parser, report_needed
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
    # resource_name =
    # number_of_fans =



    if network.lower() in ['фб', 'вк', 'ок', 'ok', 'тви', 'тытруба', 'youtube']:
        page_name = message.text.split(' ')[1].strip()
        if network.lower() == 'фб':
            fans = get_fb_fans(page_name)
        elif network.lower() == 'вк':
            fans = get_vk_fans(page_name)
        elif network.lower() == 'ок' or network.lower() == 'ok':
            fans = get_ok_fans(page_name)
        elif network.lower() == 'тви':
            fans = get_twi_fans(page_name)
        elif network.lower() == 'тытруба' or network.lower() == 'youtube':
            fans = get_youtube_fans(page_name)
        else:
            fans = 'А соцсеть то указать забыли!'
        if isinstance(fans, int):
            reply = 'В группе {} {} сейчас {} подписчиков'.format(network, page_name, fans)
        else:
            reply = fans
        bot.send_message(message.chat.id, reply)
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
