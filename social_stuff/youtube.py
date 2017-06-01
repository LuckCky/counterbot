import os

import requests

from social_stuff.groups import youtube_groups

api_key = os.environ.get('YOUTUBE_API_KEY')


def get_youtube_fans(group_name):
    try:
        group_url = youtube_groups[group_name]
    except KeyError:
        return 'В моём списке нет такой группы. Проверьте настройки или написание'
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={0}&key={1}'. \
        format(group_url, api_key)
    r = requests.get(url)
    try:
        fans = int(r.json()['items'][0]['statistics']['subscriberCount'])
    except KeyError:
        return 'Youtube вернул странный ответ, который я не могу распарсить: {}'.format(r.content)
    return fans
