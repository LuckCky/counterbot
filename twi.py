import os

import twitter

consumer_key = os.environ.get('TWI_CONSUMER_KEY')
consumer_secret = os.environ.get('TWI_CONSUMER_SECRET')
access_token = os.environ.get('TWI_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWI_ACCESS_TOKEN_SECRET')


def get_twi_fans(page_name):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

    try:
        fans = api.GetUser(screen_name=page_name).AsDict()['followers_count']
    except twitter.error.TwitterError as e:
        if e.message[0]['code'] == 50:
            return 'Неверное имя группы. Может там точку надо поставить или ru добавить?'
        else:
            return 'Ошибка: ' + e.message[0]['message']
    return fans
