import hashlib
import os
import requests

from ok_groups import ok_groups

application_id = os.environ.get('APPLICATION_ID')
application_key = os.environ.get('APPLICATION_KEY')
application_secret_key = os.environ.get('APPLICATION_SECRET_KEY')


def count_sig(group_id):
    for_sig = 'application_key=' + application_key + \
              'fields=members_countformat=jsonmethod=group.getInfouids=' \
              + group_id \
              + application_secret_key

    sig = hashlib.md5()
    sig.update(for_sig.encode())
    return sig.hexdigest()


def get_ok_fans(page_name):
    try:
        group_id = ok_groups[page_name]
    except KeyError:
        return 'В моём списке нет такой группы. Проверьте настройки или написание'
    sig = count_sig(group_id)
    url = 'https://api.ok.ru/fb.do' \
          '?application_key={0}' \
          '&fields=members_count' \
          '&format=json' \
          '&method=group.getInfo' \
          '&uids={1}' \
          '&sig={2}'.format(application_key, group_id, sig)
    r = requests.get(url)
    fans = r.json()[0]['members_count']
    return fans
