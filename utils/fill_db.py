#!/usr/bin/env python3

import xlrd
import conf
from db_works import DBWorks


def insert_aliases():
    cursor = DBWorks()

    aliases_xls = xlrd.open_workbook(conf.rambler_configs_xls, formatting_info=True)
    sheet = aliases_xls.sheet_by_name(conf.aliases_sheet)

    try:
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            cursor.cursor.execute(conf.insert_aliases, (row[0], row[1], ))
    except Exception as e:
        print(e)


def main():
    insert_aliases()
