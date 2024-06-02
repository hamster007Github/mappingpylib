#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
#general imports for testcode
import os
import logging
#unittest imports
#import unittest

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
def delete_file_if_exist(filepath:str) -> None:
    if os.path.isfile(filepath):
        os.remove(filepath)