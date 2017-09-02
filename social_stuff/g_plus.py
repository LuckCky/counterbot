#!/usr/bin/env python3

import os
import requests

import conf

token = os.environ.get('G_PLUS_TOKEN')
url_base = conf.g_plus_url_base


def get_data(url):
    try:
        r = requests.get(url_base.format(page_url=url, token=token))
    except Exception:
        r = get_data(url)
    return r


def get_g_plus_fans(page_url):
    data = get_data(page_url)
    try:
        result = data.json()["circledByCount"]
    except KeyError:
        result = data.text
    return result
