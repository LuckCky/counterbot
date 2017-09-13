#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import yaml


def get_data(url):
    error = None
    try:
        r = requests.get(url)
    except Exception as e:
        r = None
        error = e
    return error, r


def get_bloggers(url):
    full_url = 'https://www.instagram.com/{}/'.format(url)
    error, r = get_data(full_url)
    if error:
        return error
    data = BeautifulSoup(r.text, 'html.parser')
    body = data.find("body")
    script = body.find("script").get_text()
    prepared_for_dict = "".join(script.split("=")[1:])[1:-1]
    data_dict = yaml.load(prepared_for_dict)
    try:
        followed_by = data_dict["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"]
    except KeyError:
        followed_by = 0
    return followed_by
