#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
# time handling
import time
from datetime import datetime, timedelta
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
* Class: FunctionSchedulerCyclic
****************************************
'''
class FunctionScheduler():
    def __init__(self):
        self._function_list = []

    def _add_function_in_list(self, new_function_entry:dict, is_first:bool = False) -> None:
        if is_first:
            self._function_list = new_function_entry + self._function_list
        else:
            self._function_list.append(new_function_entry)

    def add_cyclic_function(self, function, cycletime_in_s:int, run_directly:bool = True, is_first:bool = False) -> None:
        ''' add a cyclic function in scheduler list. 
            function: fucntion to call cyclicly (no parameter supported)
            cycletime_in_s: cycletime in seconds
            run_directly: if True, the function will called directly with this function the first time.
            is_first: if True, the function is added az first entry in scheduler list, otherwise at last.
        '''
        if run_directly:
            next_call_datetime = datetime(2000,1,1)
        else:
            next_call_datetime = datetime.now() + timedelta(seconds=cycletime_in_s)
        scheduler_entry = {
            "fct" : function,
            "next_call" : next_call_datetime,
            "cycletime_in_s" : cycletime_in_s
        }
        self._add_function_in_list(scheduler_entry, is_first)

    def add_single_function(self, function, call_in_s:int, is_first:bool = False) -> None:
        ''' add a one time called function in scheduler list. 
            function: fucntion to call (no parameter supported)
            call_in_s: time to wait in seconds, until function is called.
            is_first: if True, the function is added az first entry in scheduler list, otherwise at last.
        '''
        scheduler_entry = {
            "fct" : function,
            "next_call" : datetime.now() + timedelta(seconds=call_in_s),
            "cycletime_in_s" : 0
        }
        self._add_function_in_list(scheduler_entry, is_first)

    def run(self, sleep_in_s:int = 1) -> None:
        ''' Scheduler function. Will not return.
            sleep_in_s: sleeptime between the scheduler is checking schedule list. Is also maximum accurency time.
        '''
        while(True):
            now = datetime.now()
            for index, entry in enumerate(self._function_list):
                if now >= entry["next_call"]:
                    #call function
                    entry["fct"]()
                    #update entry, if cyclic function, otherwise remove
                    if entry["cycletime_in_s"] > 0:
                        #cyclic function -> recalculate "next_call"
                        entry["next_call"] = now + timedelta(seconds=entry["cycletime_in_s"])
                    else:
                        #no cyclic function -> remove entry from list
                        del self._function_list[index]
            time.sleep(sleep_in_s)
