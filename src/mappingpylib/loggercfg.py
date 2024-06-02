#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
import sys
import logging
from logging.handlers import RotatingFileHandler

'''
****************************************
* Constants
****************************************
'''
VALID_LOGLEVEL = ["ERROR", "WARNING", "INFO", "DEBUG"]
VALID_LOGLEVEL_FILE = ["ERROR", "WARNING", "INFO", "DEBUG", "NONE"]

'''
****************************************
* Global variables
****************************************
'''
log = logging.getLogger(__name__)

'''
****************************************
* Classes
****************************************
'''
class LevelFilter(logging.Filter):
    '''Filters (lets through) all messages with low_level <= log message level <= high_level'''
    def __init__(self, low_level, high_level):
        self.min_level = low_level
        self.max_level = high_level

    def filter(self, record):
        is_level_matching = False
        if self.min_level <= record.levelno <= self.max_level:
            is_level_matching = True
        return is_level_matching

'''
****************************************
* Module functions
****************************************
'''
def config_logger(logger, console_loglevel = "INFO", file_loglevel = None, file_name:str = "logfile.log", file_max_mbyte:int = 10, file_backup_count:int = 5):
    #try:
    console_loglevel_num = get_numeric_loglevel(console_loglevel)
    #except Exception:
    #    raise ValueError("console_loglevel invalid")
    # console logging configuration
    formatter_console = logging.Formatter('[%(asctime)s] [%(name)12s] [%(levelname)7s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # stdout config: redirect messages everything from "console_loglevel" up to WARNING
    stdout_hdlr = logging.StreamHandler(sys.stdout)
    stdout_hdlr.setFormatter(formatter_console)
    stdout_hdlr.addFilter(LevelFilter(console_loglevel_num, logging.WARNING))
    logger.addHandler(stdout_hdlr)
    # stderr config: Redirect messages from ERROR
    stderr_hdlr = logging.StreamHandler(sys.stderr)
    stderr_hdlr.setFormatter(formatter_console)
    stderr_hdlr.addFilter(LevelFilter(logging.ERROR, logging.ERROR))
    logger.addHandler(stderr_hdlr)
    # file logging
    if file_loglevel is not None:
        #try:
        file_loglevel_num = get_numeric_loglevel(file_loglevel)
        #except Exception:
        #    raise ValueError("file_loglevel invalid")
        formatter_file = logging.Formatter('[%(asctime)s] [%(name)12s] [%(levelname)7s] %(message)s')
        file_max_byte = file_max_mbyte * (1024**2)
        file_handler = RotatingFileHandler(file_name, maxBytes=file_max_byte, backupCount=file_backup_count)
        file_handler.setLevel(file_loglevel_num)
        file_handler.setFormatter(formatter_file)
        logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

def is_valid_loglevel(loglevel):
    is_valid = False
    try:
        is_valid = any(loglevel in sub for sub in VALID_LOGLEVEL)
    except TypeError:
        log.error("TypeError in is_valid_loglevel(): shall be string")
    return is_valid

def get_numeric_loglevel(loglevel:str) -> int:
    try:
        numeric_level = getattr(logging, loglevel.upper(), None)
    except Exception:
        raise TypeError("loglevel is no string")
    if not isinstance(numeric_level, int):
        raise ValueError("invalid loglevel: %s" % loglevel)
    return numeric_level