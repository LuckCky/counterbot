#!/usr/bin/env python3

import conf
from utils.db_works import DBWorks


cursor = DBWorks()


def report_needed(message):
    if message.lower().startswith('отчёт') or message.lower().startswith('отчет'):
        return True
    return False


def message_parser(message):
    message_split = message.split(' ')
    if len(message_split) < 2:
        alias = None
    elif len(message_split) == 2:
        alias = " ".join(message_split[1:]).strip()
    else:
        alias = None
    if len(message_split) >= 3:
        network = message_split[-1].strip()
        if network.lower() not in ['фб', 'вк', 'ок', 'тви', 'ютуб']:
            network = None
            alias = " ".join(message_split[1:]).strip()
        else:
            alias = " ".join(message_split[1:-1]).strip()
    else:
        network = None
    return alias, network


def valid_resource_name(resource_name):
    return resource_name


def get_resource_name_from_alias(alias):
    aliases_list = cursor.get_info_one_arg(conf.select_one_from_aliases, "%" + alias + "%")
    if len(aliases_list) >= 2:
        return False
    if not aliases_list:
        return None
    return aliases_list[0][0]


def get_fans_count(resource_name, network_name):
    number_of_fans = 0
    network_list = []
    print(resource_name)
    print(network_name)
    if not network_name:
        network_list = ['фб', 'вк', 'ок', 'тви', 'ютуб']
    else:
        network_list.append(network_name)
    for element in network_list:
        print(element)
        args = (resource_name, element,)
        resource_id = cursor.get_info_two_args(conf.select_resource_id, *args)[0]
        print(resource_id)
        fans = conf.number_of_fans[element]
        number_of_fans += fans(resource_id)
    return number_of_fans
