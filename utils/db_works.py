#!/usr/bin/python3
import os
import urllib.parse
import psycopg2

import conf


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