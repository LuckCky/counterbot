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
            aliases_list = row[1].split(",")
            cursor.cursor.execute(conf.insert_aliases, (row[0], aliases_list,))
    except Exception as e:
        print(e)
    finally:
        cursor.connection.commit()


def main():
    insert_aliases()

if __name__ == "__main__":
    main()
