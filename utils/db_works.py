#!/usr/bin/python3
import os
import urllib.parse
import psycopg2

import conf


class DBWorks(object):
    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def fire_up_db(self):
        try:
            self.cursor.execute(conf.create_aliases_table)
            self.connection.commit()
        except psycopg2.ProgrammingError:
            self.connection.rollback()
        try:
            self.cursor.execute(conf.create_ids_table)
            self.connection.commit()
        except psycopg2.ProgrammingError:
            self.connection.rollback()
        try:
            self.cursor.execute(conf.create_users_count_table)
            self.connection.commit()
        except psycopg2.ProgrammingError:
            self.connection.rollback()
        finally:
            self.connection.close()
