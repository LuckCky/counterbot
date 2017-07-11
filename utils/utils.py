#!/usr/bin/env python3

import datetime

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
        network = message_split[-1].strip().lower()
        if network not in conf.network_list:
            network = None
            alias = " ".join(message_split[1:]).strip()
        else:
            alias = " ".join(message_split[1:-1]).strip()
    else:
        network = None
    return alias, network


def get_resource_name_from_alias(alias):
    aliases_list = cursor.get_info_one_arg(conf.select_one_from_aliases, "%" + alias.lower() + "%")
    if len(aliases_list) >= 2:
        return False
    if not aliases_list:
        return None
    return aliases_list[0][0]


def get_fans_count(resource_name, network_name):
    number_of_fans = 0
    network_list = []
    error_text = ''
    if not network_name:
        network_list = conf.network_list
    else:
        network_list.append(network_name)
    for element in network_list:
        args = (resource_name, element,)
        resource_id = cursor.get_info_with_args(conf.select_resource_id_by_name, args)
        if not resource_id:
            break
        resource_id = resource_id[0][0]
        fans = conf.number_of_fans[element](resource_id)
        if isinstance(fans, str):
            error_text += fans
        elif isinstance(fans, (float, int, )):
            number_of_fans += fans
    return number_of_fans, error_text


def get_project_names_list():
    projects = cursor.get_info_no_args(conf.select_all_names_from_aliases)
    project_names_list = []
    for project in projects:
        project_names_list.append(project[0])
    return project_names_list


def get_all_fans_count(project_names_list):
    networks_list = conf.network_list
    result = []
    for project_name in project_names_list:
        sub_result = []
        number_of_fans = 0
        for network_name in networks_list:
            args = (project_name, network_name,)
            print(args)
            project_id = cursor.get_info_with_args(conf.select_resource_id_by_project, args)
            print(project_id)
            if project_id:
                for _id in project_id:
                    fans = conf.number_of_fans[network_name](_id[1])
                    print('fans', fans)
                    if isinstance(fans, str):
                        sub_result.append("По проекту {} произошла ошибка {}.".
                                          format(project_name, fans))
                    elif isinstance(fans, (float, int,)):
                        number_of_fans += fans
                print('number_of_fans', number_of_fans)
                sub_result.append("По проекту {} количество подписчиков {}.".
                                  format(project_name, number_of_fans))
            now = datetime.datetime.now()
            error = cursor.insert_info(conf.insert_data, (project_id[0][0], now, number_of_fans))
            if error:
                sub_result.append("По проекту {} произошла ошибка при записи в БД {}.".
                                  format(project_name, error))
        n = 1
        print(result, n)
        n += 1
        result.append(sub_result)
    return result
