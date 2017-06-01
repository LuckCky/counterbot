#!/usr/bin/python3


def report_needed(message):
    if message.lower().startswith('отчёт') or message.lower().startswith('отчет'):
        return True
    return False


def message_parser(message):
    resource_name = message.split(' ')[1].strip()
    if len(message.split(' ')) >= 3:
        network = message.split(' ')[2].strip()
    else:
        network = None
    return resource_name, network
