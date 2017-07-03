import hashlib
import os

import requests

from social_stuff.groups import ok_groups

application_id = os.environ.get('OK_APPLICATION_ID')
application_key = os.environ.get('OK_APPLICATION_KEY')
application_secret_key = os.environ.get('OK_APPLICATION_SECRET_KEY')


def count_sig(group_id):
    for_sig = 'application_key=' + application_key + \
              'fields=members_countformat=jsonmethod=group.getInfouids=' \
              + group_id \
              + application_secret_key

    sig = hashlib.md5()
    sig.update(for_sig.encode())
    return sig.hexdigest()


def get_ok_fans(group_id ):
    sig = count_sig(group_id)
    url = 'https://api.ok.ru/fb.do' \
          '?application_key={0}' \
          '&fields=members_count' \
          '&format=json' \
          '&method=group.getInfo' \
          '&uids={1}' \
          '&sig={2}'.format(application_key, group_id, sig)
    r = requests.get(url)
    try:
        fans = r.json()[0]['members_count']
    except KeyError:
        return 'ODNOKLASSNIKI вернули странный ответ, который я не могу распарсить: {}'.format(r.content)
    return fans
