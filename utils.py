#!/usr/bin/python3
import os
import urllib.parse
import psycopg2

import conf


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


def fire_up_db():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = connection.cursor()
    cursor.execute(conf.create_aliases_table)
    try:
        cursor.execute(conf.create_aliases_table)
        connection.commit()
    except psycopg2.ProgrammingError:
        connection.rollback()
    try:
        cursor.execute(conf.create_ids_table)
        connection.commit()
    except psycopg2.ProgrammingError:
        connection.rollback()
    try:
        cursor.execute(conf.create_users_count_table)
        connection.commit()
    except psycopg2.ProgrammingError:
        connection.rollback()
    finally:
        connection.close()
