#!/usr/bin/env python3

import os

import requests
from set_vars import set_vars
set_vars()

api_key = os.environ.get('YOUTUBE_API_KEY')


def get_youtube_fans(group_url):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={0}&key={1}'. \
        format(group_url, api_key)
    r = requests.get(url)
    try:
        fans = int(r.json()['items'][0]['statistics']['subscriberCount'])
    except KeyError:
        return 'Youtube вернул странный ответ, который я не могу распарсить: {}'.format(r.content)
    return fans
