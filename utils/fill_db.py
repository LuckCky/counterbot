#!/usr/bin/env python3

import os
import urllib.parse
import psycopg2
import xlrd

import conf
from utils.db_works import DBWorks

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


def insert_aliases():
    # cursor = DBWorks()

    aliases_xls = xlrd.open_workbook(conf.rambler_configs_xls, formatting_info=True)
    sheet = aliases_xls.sheet_by_name(conf.aliases_sheet)

    # check if aliases record exist
    cursor.execute(conf.select_all_aliases)
    # if yes, don't insert any
    if cursor.fetchall():
        return

    try:
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            cursor.cursor.execute(conf.insert_aliases, (row[0], row[1], ))
    except Exception as e:
        print(e)


def main():
    insert_aliases()
