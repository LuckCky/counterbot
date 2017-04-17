import cherrypy
import os
import random
import time

import telebot

import conf
from fb import get_fb_fans
from vk_info import get_vk_fans

token = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

WEBHOOK_PORT = int(os.environ.get('PORT', '5000'))
WEBHOOK_LISTEN = conf.webhook_listen

WEBHOOK_URL_BASE = conf.post_url
WEBHOOK_URL_PATH = "/{}/".format(token)

bot = telebot.TeleBot(token)


def choose_message(messages, end_random=50):
    num = random.randint(0, end_random)
    if num < len(messages):
        return messages[num]
    else:
        return None


@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
                                    'voice', 'location', 'contact'])
def echo_all(message):
    if message.text.startswith('отчёт') or message.text.startswith('отчет') \
            or message.text.startswith('Отчет') or message.text.startswith('Отчёт'):
        command = message.text.split(':')[1].strip()
        print('command', command)
        if len(command.split(' ')) < 2:
            bot.send_message(message.chat.id, "Чёт мне не хватает. То ли названия соцсети, то ли группы")
            return
        elif len(command.split(' ')) > 3:
            bot.send_message(message.chat.id, "Чёт мне мне лишнего пишете")
            return
        print(command.split(' '))
        network, page_name = command.split(' ').strip()
        print(network)
        print(page_name)
        if network.lower() == 'фб':
            fans = get_fb_fans(page_name)
        elif network.lower() == 'вк':
            fans = get_vk_fans(page_name)
        else:
            fans = 'А соцсеть то указать забыли!'
        if isinstance(fans, int):
            reply = 'В группе {} {} сейчас {} подписчиков'.format(network, page_name, fans)
        else:
            reply = fans
        bot.send_message(message.chat.id, reply)
        return
    bot.send_message(message.chat.id, message.text)


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
