#!/usr/bin/env python3

import xlrd

import conf
from utils.db_works import DBWorks


def insert_aliases():
    cursor = DBWorks()

    aliases_xls = xlrd.open_workbook(conf.rambler_configs_xls, formatting_info=True)
    sheet = aliases_xls.sheet_by_name(conf.aliases_sheet)

    # check if aliases records exist
    cursor.cursor.execute(conf.select_all_aliases)
    # if yes, don't insert any
    if cursor.cursor.fetchall():
        return

    try:
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            cursor.cursor.execute(conf.insert_aliases, (row[0], row[1],))
    except Exception as e:
        print(e)
    finally:
        cursor.connection.commit()


def insert_ids():
    cursor = DBWorks()

    aliases_xls = xlrd.open_workbook(conf.rambler_configs_xls, formatting_info=True)
    sheet = aliases_xls.sheet_by_name(conf.ids_sheet)

    # check if ids records exist
    cursor.cursor.execute(conf.select_all_ids)
    # if yes, don't insert any
    if cursor.cursor.fetchall():
        return

    try:
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            cursor.cursor.execute(conf.insert_resource_ids, (
                int(row[1]), row[2], row[3], row[4], row[5],))
    except Exception as e:
        print(e)
    finally:
        cursor.cursor.connection.commit()


def main():
    insert_aliases()
    insert_ids()

if __name__ == "__main__":
    main()
