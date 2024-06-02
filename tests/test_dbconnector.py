#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
# general imports for testcode
import logging
# unittest imports
import unittest
#from unittest.mock import patch
#from pretend import stub
# import code under test
#import mappingpylib.dbconnector
from mappingpylib.dbconnector import DbConnector

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
class Test_dbconnector(unittest.TestCase):
    def setUp(self):
        #blub
        pass

    def test_test_execute_query_invalidhost(self):
        db_config = {
            "host":"invalidhost",
            "db_name":"test_db",
            "username":"username",
            "password":"password",
            "port":3306
        }
        test_db = DbConnector(**db_config)
        query_str = ""
        is_commit = False
        disconnect = True
        result = test_db.execute_query(query=query_str, commit=is_commit, disconnect=disconnect)
        self.assertIsNone(result)

    @unittest.skip("only for development")
    def test_test_execute_query_realworld(self):
        db_config = {
            "host":"localhost",
            "db_name":"test_db",
            "username":"username",
            "password":"password",
            "port":3306
        }
        test_db = DbConnector(**db_config)
        query_str = "SELECT * FROM account"
        is_commit = False
        disconnect = True
        result = test_db.execute_query(query=query_str, commit=is_commit, disconnect=disconnect)
        self.assertIsNotNone(result)
'''
****************************************
* Public functions
****************************************
'''
