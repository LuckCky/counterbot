#!/usr/bin/env python3

import os
import psycopg2

import conf
from logger import init_logger
from set_vars import set_vars

db_logger = init_logger('db logger')
set_vars()

db_logger.info('environment variables set')

url = os.environ.get("DATABASE_URL")
db_logger.info('environment variables read')


class DBWorks(object):
    def __init__(self):
        db_logger.info('initializing db connection')
        self.connection = psycopg2.connect(url)
        self.cursor = self.connection.cursor()
        db_logger.info('connected to db')

    def fire_up_db(self):
        db_logger.info('preparing to fire up db')
        try:
            self.cursor.execute(conf.create_aliases_table)
            self.connection.commit()
            db_logger.info('aliases table created')
        except psycopg2.ProgrammingError:
            db_logger.info('aliases table exists')
            self.connection.rollback()
        try:
            self.cursor.execute(conf.create_ids_table)
            self.connection.commit()
            db_logger.info('ids table created')
        except psycopg2.ProgrammingError:
            db_logger.info('ids table exists')
            self.connection.rollback()
        try:
            self.cursor.execute(conf.create_users_count_table)
            self.connection.commit()
            db_logger.info('users count table created')
        except psycopg2.ProgrammingError:
            db_logger.info('users count table exists')
            self.connection.rollback()
        try:
            self.cursor.execute(conf.create_all_users_table)
            self.connection.commit()
            db_logger.info('all users table created')
        except psycopg2.ProgrammingError:
            db_logger.info('all users table exists')
            self.connection.rollback()
        finally:
            self.connection.close()
            db_logger.info('connection closed after firing db up')

    def get_info_no_args(self, statement):
        try:
            self.cursor.execute(statement)
            db_logger.info('db cursor executed no args. Statement: {}'.format(statement))
            return self.cursor.fetchall()
        except psycopg2.Error as error:
            db_logger.error('no args error: {}'.format(error.pgerror))

    def get_info_one_arg(self, statement, value):
        try:
            self.cursor.execute(statement, (value,))
            db_logger.info('db cursor executed one arg: {}. Statement: {}'.format(value, statement))
            return self.cursor.fetchall()
        except psycopg2.Error as error:
            db_logger.error('one arg error: {}'.format(error.pgerror))

    def get_info_with_args(self, statement, args):
        try:
            self.cursor.execute(statement, args)
            db_logger.info('db cursor executed with args: {}. Statement: {}'.format(str(args), statement))
            return self.cursor.fetchall()
        except psycopg2.Error as error:
            db_logger.error('some args error: {}'.format(error.pgerror))

    def insert_info(self, statement, args):
        try:
            self.cursor.execute(statement, args)
            db_logger.info('db insert executed with args: {}. Statement: {}'.format(str(args), statement))
            self.connection.commit()
        except psycopg2.Error as error:
            self.connection.rollback()
            db_logger.error('db insert error: {}'.format(error.pgerror))
            return error
        return None


if __name__ == '__main__':
    DBWorks().fire_up_db()
