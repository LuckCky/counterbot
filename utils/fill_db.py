#!/usr/bin/env python3

import xlrd

import conf
from logger import init_logger
from utils.db_works import DBWorks

fill_db_logger = init_logger('fill db logger')


def insert_aliases():
    cursor = DBWorks()
    fill_db_logger.info('cursor for insert aliases initialized')

    aliases_xls = xlrd.open_workbook(conf.rambler_configs_xls, formatting_info=True)
    sheet = aliases_xls.sheet_by_name(conf.aliases_sheet)
    fill_db_logger.info('xls opened and read')

    # check if aliases records exist
    cursor.cursor.execute(conf.select_all_aliases)
    # if yes, don't insert any
    if cursor.cursor.fetchall():
        fill_db_logger.info('records in aliases table exist')
        return

    try:
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            cursor.cursor.execute(conf.insert_aliases, (row[0], row[1].lower(),))
            fill_db_logger.info('aliases table filled up')
    except Exception as e:
        print(e)
        fill_db_logger.error('errors during filling aliases: {}'.format(e))
    finally:
        cursor.connection.commit()
        fill_db_logger.info('connection closed after filling aliases')


def insert_ids():
    cursor = DBWorks()
    fill_db_logger.info('cursor for insert ids initialized')

    aliases_xls = xlrd.open_workbook(conf.rambler_configs_xls, formatting_info=True)
    sheet = aliases_xls.sheet_by_name(conf.ids_sheet)
    fill_db_logger.info('xls opened and read')

    # check if ids records exist
    cursor.cursor.execute(conf.select_all_ids)
    # if yes, don't insert any
    if cursor.cursor.fetchall():
        fill_db_logger.info('records in ids table exist')
        return

    try:
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            cursor.cursor.execute(conf.insert_resource_ids, (
                int(row[1]), row[2], row[3], row[4], row[5].split('/')[-1],))
            fill_db_logger.info('ids table filled up')
    except Exception as e:
        fill_db_logger.error('errors during filling ids: {}'.format(e))
    finally:
        cursor.cursor.connection.commit()
        fill_db_logger.info('connection closed after filling ids')


def main():
    insert_aliases()
    insert_ids()


if __name__ == "__main__":
    main()
