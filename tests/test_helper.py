#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
import unittest
from datetime import timedelta
from mappingpylib import helper

'''
****************************************
* Global variables
****************************************
'''
#log = logging.getLogger(__name__)

'''
****************************************
* Classes
****************************************
'''
class Test_Helper_isElementInList(unittest.TestCase):
    def test_match_one_element(self):
        testlist = ["testtext"]
        self.assertTrue(helper.isElementInList(testlist,"testtext"))
    def test_match_first_element(self):
        testlist = ["testtext", "other1", "other2"]
        self.assertTrue(helper.isElementInList(testlist,"testtext"))
    def test_match_last_element(self):
        testlist = ["other1", "other2", "testtext"]
        self.assertTrue(helper.isElementInList(testlist,"testtext"))
    def test_nomatch_other_one_element(self):
        testlist = ["other"]
        self.assertFalse(helper.isElementInList(testlist,"testtext"))
    def test_nomatch_other_multiple_element(self):
        testlist = ["other1", "other2", "other3"]
        self.assertFalse(helper.isElementInList(testlist,"testtext"))
    def test_nomatch_addpost(self):
        testlist = ["testtext1", "other"]
        self.assertFalse(helper.isElementInList(testlist,"testtext"))
    def test_nomatch_addpre(self):
        testlist = ["1testtext", "other"]
        self.assertFalse(helper.isElementInList(testlist,"testtext"))
    def test_empty_list(self):
        testlist = [] 
        self.assertFalse(helper.isElementInList(testlist,"testtext"))

class Test_Helper_pretty_byte(unittest.TestCase):
    def test_input_byte(self):
        self.assertEqual(helper.pretty_byte(500), "500b")
    def test_input_1kilobyte(self):
        self.assertEqual(helper.pretty_byte(1024**1), "1.0kb")
    def test_input_100kilobyte(self):
        self.assertEqual(helper.pretty_byte((100*1024)+400), "100.4kb")
    def test_input_1megabyte(self):
        self.assertEqual(helper.pretty_byte(1024**2), "1.0mb")
    def test_input_1gigabyte(self):
        self.assertEqual(helper.pretty_byte(1024**3), "1.0gb")
    def test_input_1terabyte(self):
        self.assertEqual(helper.pretty_byte(1024**4), "1024.0gb")
    def test_input_wrong_type(self):
        self.assertEqual(helper.pretty_byte("teststring"), "NaN")

class Test_Helper_pretty_deltatime(unittest.TestCase):
    def test_input_7s(self):
        timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        timediff = timedelta(seconds=7)
        self.assertEqual(helper.pretty_deltatime(timediff), "7s")
    def test_input_60s(self):
        timediff = timedelta(seconds=60)
        self.assertEqual(helper.pretty_deltatime(timediff), "1m")
    def test_input_1min(self):
        timediff = timedelta(minutes=1)
        self.assertEqual(helper.pretty_deltatime(timediff), "1m")
    def test_input_5h(self):
        timediff = timedelta(hours=5)
        self.assertEqual(helper.pretty_deltatime(timediff), "5h")
    def test_input_23h_59min(self):
        timediff = timedelta(hours=23, minutes=59)
        self.assertEqual(helper.pretty_deltatime(timediff), "23h")
    def test_input_1day(self):
        timediff = timedelta(days=1)
        self.assertEqual(helper.pretty_deltatime(timediff), "1d")
    def test_input_370days(self):
        timediff = timedelta(days=370)
        self.assertEqual(helper.pretty_deltatime(timediff), "370d")
    def test_input_wrong_type(self):
        self.assertEqual(helper.pretty_deltatime(5), "N/A")

'''
****************************************
* Public functions
****************************************
'''
