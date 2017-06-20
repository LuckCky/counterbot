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
    if len(message_split) >= 2:
        alias = message_split[1].strip()
    else:
        alias = None
    if len(message_split) >= 3:
        network = message_split[-1].strip()
    else:
        network = None
    return alias, network


def valid_resource_name(resource_name):
    return resource_name


def get_resource_name_from_alias(alias):
    print("!!!!!!!!!STARTED get_resource_name_from_alias")
    aliases_list = cursor.get_info_no_args(conf.select_all_aliases)
    for element in aliases_list:
        if alias in element[2]:
            resource_name = element[1]
            return resource_name
    # aliases_list = cursor.get_info_one_arg(conf.select_one_from_aliases, alias)
    # return aliases_list[0]
