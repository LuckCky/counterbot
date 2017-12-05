#!/usr/bin/env python3

import datetime

import conf
from logger import init_logger
from utils.db_works import DBWorks

utils_logger = init_logger('utils logger')
cursor = DBWorks()

utils_logger.info('cursor for utils initialized')


def report_needed(message):
    """
    decide if user wants report in his message
    :param message: user message
    :return: true or false
    """
    if message.lower().startswith('отчёт') or message.lower().startswith('отчет'):
        utils_logger.info('report needed for message: {}'.format(message))
        return True
    return False


def message_parser(message):
    """
    parse message if user sent alias and/or network
    :param message: user message
    :return: alias, network or None
    """
    utils_logger.info('message parser started')
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
    utils_logger.info('message parsed. Alias is {}, network is {}'.format(str(alias), str(network)))
    return alias, network


def get_resource_name_from_alias(alias):
    """
    get resources names from DB by their aliases
    :param alias:
    :return:
    """
    utils_logger.info('getting resource name from alias {}'.format(alias))
    aliases_list = cursor.get_info_one_arg(conf.select_one_from_aliases, "%" + alias.lower() + "%")
    if len(aliases_list) >= 2:
        utils_logger.info('returning False')
        return False
    if not aliases_list:
        utils_logger.info('returning None')
        return None
    utils_logger.info('returning aliases list {}'.format(str(aliases_list[0][0])))
    return aliases_list[0][0]


def get_fans_count(resource_name, network_name):
    utils_logger.info('starting get fans count')
    number_of_fans = 0
    network_list = []
    error_text = ''
    network = None
    if not network_name:
        network_list = conf.network_list
    else:
        network_list.append(network_name)
    utils_logger.info('network list {}'.format(str(network_list)))
    for element in network_list:
        args = (resource_name, element,)
        resource_id = cursor.get_info_with_args(conf.select_resource_id_by_name, args)
        if resource_id:
            resource_id = resource_id[0][0]
            fans = conf.number_of_fans[element](resource_id)
            utils_logger.info('got fans count')
            if isinstance(fans, str):
                error_text += fans
                network = element
                utils_logger.info('got error {} for network {}'.format(fans, network))
            elif isinstance(fans, (float, int, )):
                number_of_fans += fans
    utils_logger.info('returning all fans count, error text and networks')
    return number_of_fans, error_text, network


def get_project_names_list():
    utils_logger.info('starting getting project names list')
    # projects = cursor.get_info_no_args(conf.select_all_names_from_aliases)
    projects = cursor.get_info_no_args(conf.select_all_names_from_resource_ids)
    utils_logger.info('got project from db {}'.format(str(projects)))
    project_names_list = []
    for project in projects:
        project_names_list.append(project[0]) if project[0] not in project_names_list else None
    utils_logger.info('returning projects names list {}'.format(str(project_names_list)))
    return project_names_list


def get_all_fans_count(project_names_list):
    utils_logger.info('starting get all fans count for project(s)'.format(str(project_names_list)))
    networks_list = conf.network_list
    result = []
    total_number_of_fans = 0
    for project_name in project_names_list:
        sub_result = []
        error_result = []
        number_of_fans = 0
        total_fans_last_time = 0
        for network_name in networks_list:
            args = (project_name, network_name,)
            project_data = cursor.get_info_with_args(conf.select_resource_id_by_project, args)
            if project_data:
                project_network_fans = 0
                for _id in project_data:
                    fans = conf.number_of_fans[network_name](_id[1])
                    if isinstance(fans, str):
                        error_result.append("По проекту {} произошла ошибка '{}' в соцсети {}.".
                                            format(project_name, fans, network_name))
                    elif isinstance(fans, (float, int,)):
                        number_of_fans += fans
                        project_network_fans += fans
                now = datetime.datetime.now()
                error = cursor.insert_info(conf.insert_data, (project_data[0][0], now, project_network_fans))
                if error:
                    sub_result.append("По проекту {} произошла ошибка при записи в БД '{}'.".
                                      format(project_name, error))
                args = (project_data[0][0], )
                fans_last_time = cursor.get_info_one_arg(conf.select_previous_count_of_fans, args)
                total_fans_last_time += int(fans_last_time[1][3])
        if total_fans_last_time != 0:
            fans_diff = number_of_fans - total_fans_last_time
            sub_result.append("По проекту {} количество подписчиков {}. ({})".
                              format(project_name, number_of_fans, fans_diff))
        else:
            sub_result.append("По проекту {} количество подписчиков {}. Разницу посчитать не смог".
                              format(project_name, number_of_fans))
        total_number_of_fans += number_of_fans
        result.append(sub_result)
        if error_result:
            result.append(error_result)
    result.append("Общее число подписчиков по всем проектам: {}.".format(total_number_of_fans))
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(1)
    yesterday_fans_record = cursor.get_info_one_arg(conf.select_all_user_per_date, yesterday)
    if not yesterday_fans_record:
        yesterday_fans_record = cursor.get_info_no_args(conf.select_last_users_data)
    error = cursor.insert_info(conf.insert_all_users_data, (now, total_number_of_fans))
    if error:
        result.append("Произошла ошибка при записи в БД общего числа пользователей: '{}'.".
                      format(error))
    fans_diff = total_number_of_fans - yesterday_fans_record[0][2]
    previous_date = yesterday_fans_record[0][1].strftime("%Y-%m-%d %H:%M")
    result.append("Разница количества подписчиков с {} составила {}.".
                  format(previous_date, fans_diff))
    utils_logger.info('returning all fans count result: {}'.format(str(result)))
    return result


def get_report_size(text):
    utils_logger.info('starting get report size')
    if text.lower() == "отчет" or text.lower() == "отчёт":
        utils_logger.info('returning BIG report')
        return "big"
    utils_logger.info('returning None')
    return None
