#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import List, Generic
# other
from datetime import timedelta
# logging
import logging

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

'''
****************************************
* Public functions
****************************************
'''
def pretty_deltatime(timediff_timedelta:timedelta) -> str:
    '''convert timedelta into a simple string like:
                 input < 60 s = "#s"
      1 min <= input < 60 min = "#m"
    1 hour <= input < 24 hour = "#h"
               1 day <= input = "#d"
    In case of not supported input, this function returns string "N/A"
    '''
    prettystr = "N/A"
    try:
        seconds = timediff_timedelta.seconds
        days = timediff_timedelta.days
        if days >= 1:
            prettystr = f"{days}d"
        elif seconds < 60:
            prettystr = f"{seconds}s"
        elif seconds < 3600:
            prettystr = f"{int(seconds/60)}m"
        else:
            prettystr = f"{int(seconds/3600)}h"
    except AttributeError:
        log.error("AttributeError in pretty_deltatime(): input is no timedelta object")
    except Exception: # pragma: no cover
        log.exception("Unexpected exception in pretty_deltatime()")
    return prettystr



def pretty_byte(size_in_byte:int) -> str:
    '''convert number byte integer into a simple string like:
                         input < 1.024 = "#b"
            1.024 <= input < 1.048.576 = "#.#kb"
    1.048.576 <= input < 1.073.741.824 = "#.#mb"
                1.073.741.824 <= input = "#.#gb"
    In case of not supported input, this function returns string "NaN"
    '''

    prettystr = "NaN"
    try:
        size_in_gigabyte = size_in_byte / float(1024**3)
        size_in_megabyte = size_in_byte / float(1024**2)
        size_in_kilobyte = size_in_byte / float(1024**1)
        if size_in_gigabyte >= 1.0:
            prettystr = f"{size_in_gigabyte:.1f}gb"
        elif size_in_megabyte >= 1.0:
            prettystr = f"{size_in_megabyte:.1f}mb"
        elif size_in_kilobyte >= 1.0:
             prettystr = f"{size_in_kilobyte:.1f}kb"
        else:
            prettystr = f"{size_in_byte}b"
    except TypeError:
        log.error("TypeError in pretty_byte()")
    except Exception: # pragma: no cover
        log.exception("Unexpected exception in pretty_byte()")
    return prettystr

def isElementInList(element_list:List, element_to_search:Generic) -> bool:
    '''check if exact element_to_search is part of element_list:
    Can be used e.g. to find exact string because blabla in list will also return if blabla is only part of a entry.
    return:
        True: element found in list
        False: element not found in list
    '''
    found = False
    if element_list:
        for element in element_list:
            if element == element_to_search:
                found = True
                break
    return found

