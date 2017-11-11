#!/usr/bin/env python3

import logging
import logging.handlers
import os


def create_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)


def init_logger(logger_name):
    _logger = logging.getLogger(logger_name)
    log_dir = './logs'
    log_file = './logs/bot.log'

    try:
        file_handler = logging.handlers.RotatingFileHandler(filename=log_file,
                                                            maxBytes=10485760,
                                                            backupCount=5)
        syslog_handler = logging.FileHandler(filename=log_file)

    except IOError:
        create_dir(name='logs')
        create_dir(name=log_dir)
        file_handler = logging.handlers.RotatingFileHandler(filename=log_file,
                                                            maxBytes=10485760,
                                                            backupCount=5)
        syslog_handler = logging.FileHandler(filename=log_file)

    log_formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%m/%d/%Y %H:%M:%S')
    file_handler.setFormatter(log_formatter)
    syslog_handler.setFormatter(log_formatter)

    _logger.addHandler(file_handler)
    _logger.addHandler(syslog_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    _logger.addHandler(console_handler)

    _logger.setLevel(logging.DEBUG)

    return _logger


if __name__ == '__main__':
    logger = init_logger("Test_Listener")
    logger.error('Error here')
