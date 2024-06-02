#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
#general imports for testcode
import logging
#unittest imports
import unittest
import misc
#import code under test
from mappingpylib import msgidcache


'''
****************************************
* Global variables
****************************************
'''
log = logging.getLogger(__name__)
tmp_msgidcache_file = "./tests/.test_msgid_cache"

'''
****************************************
* Classes
****************************************
'''
class Test_MsgIdCache(unittest.TestCase):
    def setUp(self):
        misc.delete_file_if_exist(tmp_msgidcache_file)

    def test_msgidcache_set_get_without_thread(self):
        mymsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        mymsgidcache.set_message_id("chat1", 0, 123456)
        msg_id = mymsgidcache.get_message_id("chat1")
        self.assertEqual(msg_id, 123456)

    def test_msgidcache_set_get_thread(self):
        mymsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        mymsgidcache.set_message_id("chat1", 5, 123456)
        msg_id = mymsgidcache.get_message_id("chat1", 5)
        self.assertEqual(msg_id, 123456)

    def test_msgidcache_set_get_none_chat(self):
        mymsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        mymsgidcache.set_message_id("chat1", 5, 123456)
        msg_id = mymsgidcache.get_message_id("chat2", 5)
        self.assertIsNone(msg_id)

    def test_msgidcache_set_get_none_thread(self):
        mymsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        mymsgidcache.set_message_id("chat1", 5, 123456)
        msg_id = mymsgidcache.get_message_id("chat1", 0)
        self.assertIsNone(msg_id)

    def test_msgidcache_get_wrong_chatid_type(self):
        mymsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        msg_id = mymsgidcache.get_message_id(123456)
        self.assertIsNone(msg_id)

    def test_msgidcache_get_wrong_threadid_type(self):
        mymsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        msg_id = mymsgidcache.get_message_id("chat1", "1")
        self.assertIsNone(msg_id)

    def test_msgidcache_store_restore(self):
        testmsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        testmsgidcache.set_message_id("chat1", 0, 123456)
        testmsgidcache.store_cache()
        del testmsgidcache
        new_testmsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        new_testmsgidcache.restore_cache()
        msg_id = new_testmsgidcache.get_message_id("chat1")
        self.assertEqual(msg_id, 123456)

    def test_msgidcache_restore_missing_file(self):
        testmsgidcache = msgidcache.MsgIdCache(tmp_msgidcache_file)
        with self.assertLogs("mappingpylib.msgidcache", level="WARNING") as cm:
            testmsgidcache.restore_cache()
        has_logentries = len(cm.output) > 0
        self.assertTrue(has_logentries)
        if has_logentries:
            self.assertIn("load .msgid_cache failed. exception:", cm.output[0])

    def test_msgidcache_wrong_filename_type(self):
        self.assertRaises(TypeError, msgidcache.MsgIdCache(1))

'''
****************************************
* Public functions
****************************************
'''
