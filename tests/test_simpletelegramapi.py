#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
# general imports for testcode
import logging
import json
# unittest imports
import unittest
from unittest.mock import patch
from pretend import stub
# import code under test
import mappingpylib.simpletelegramapi
from mappingpylib.simpletelegramapi import SimpleTelegramApi

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
class Test_simpletelegramapi(unittest.TestCase):
    def setUp(self):
        #blub
        pass

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_send_message_ok(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_ok({"message_id":123456})
        success, msgid = test_api.send_message(chat_id = "123456789", text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertTrue(success)
        self.assertEqual(msgid, 123456)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_send_message_ok_long(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_ok({"message_id":123456})
        success, msgid = test_api.send_message(chat_id = "123456789", text = ("x"*10000), parse_mode="HTML")
        self.assertTrue(success)
        self.assertEqual(msgid, 123456)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_send_message_error(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_error(401, "An error description text")
        success, msgid = test_api.send_message(chat_id = "123456789", text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertFalse(success)
        self.assertIsNone(msgid)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_send_message_thread_ok(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_ok({"message_id":123456})
        success, msgid = test_api.send_message_thread(chat_id = "123456789", message_thread_id = 99, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertTrue(success)
        self.assertEqual(msgid, 123456)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_send_message_thread_error(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_error(401, "An error description text")
        success, msgid = test_api.send_message_thread(chat_id = "123456789", message_thread_id = 99, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertFalse(success)
        self.assertIsNone(msgid)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_edit_message_ok(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_ok({"message_id":123456})
        success = test_api.edit_message(chat_id = "123456789", message_id = 123456, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertTrue(success)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_edit_message_error(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_error(401, "An error description text")
        success = test_api.edit_message(chat_id = "123456789", message_id = 123456, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertFalse(success)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_edit_message_nomodification(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_error(400, mappingpylib.simpletelegramapi.ERROR_DESC_NO_MODIFICATION)
        success = test_api.edit_message(chat_id = "123456789", message_id = 123456, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertTrue(success)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_delete_message_ok(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_ok({"message_id":123456})
        success = test_api.delete_message(chat_id = "123456789", message_id = 123456)
        self.assertTrue(success)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_delete_message_error(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_error(401, "An error description text")
        success = test_api.delete_message(chat_id = "123456789", message_id = 123456)
        self.assertFalse(success)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_pin_message_ok(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_ok({"message_id":123456})
        success = test_api.pin_message(chat_id = "123456789", message_id = 123456)
        self.assertTrue(success)

    @patch("mappingpylib.simpletelegramapi.requests")
    def test_pin_message_error(self, mock_requests):
        test_api = SimpleTelegramApi("1234567890:abcdefgABCDEFG1234567890")
        #setup stub for requests module
        mock_requests.get.return_value = generatestub_requests_get_response_error(401, "An error description text")
        success = test_api.pin_message(chat_id = "123456789", message_id = 123456)
        self.assertFalse(success)

    def test_util_smart_trim_text_notrim(self):
        untrimmed_text = "First line text\nSecond line text\nThird line text\n"
        trimmed_text = SimpleTelegramApi.util_smart_trim_text(text = untrimmed_text, trim_end_str = "...", trim_str = "\n")
        self.assertEqual(trimmed_text, untrimmed_text)

    def test_util_smart_trim_text_defaults(self):
        end_str = "..."
        untrimmed_text = "First line text\nSecond line text\nThird line text\n" + ("x" * 10000)
        trimmed_text = SimpleTelegramApi.util_smart_trim_text(text = untrimmed_text, trim_end_str = "...", trim_str = "\n")
        self.assertEqual(trimmed_text, "First line text\nSecond line text\nThird line text" + end_str)

    def test_util_smart_trim_text_whitespace(self):
        end_str = "..."
        untrimmed_text = "First line text\nSecond line text\nThird line text\n" + ("x" * 10000)
        trimmed_text = SimpleTelegramApi.util_smart_trim_text(text = untrimmed_text, trim_end_str = end_str, trim_str = " ")
        self.assertEqual(trimmed_text, "First line text\nSecond line text\nThird line" + end_str)

    @unittest.skip("only for development")
    def test_send_message_realworld(self):
        chat_id = "11111"
        bot_token = "11111"
        test_api = SimpleTelegramApi(bot_token)
        success, msgid = test_api.send_message(chat_id = chat_id, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertTrue(success)
        success = test_api.edit_message(chat_id = chat_id, message_id = msgid, text = "This is a test text with special signs / and &", parse_mode="HTML")
        self.assertTrue(success)
'''
****************************************
* Public functions
****************************************
'''

# This method will be used by the mock to replace requests.get
def generatestub_requests_get_response_ok(result_dict:dict):
    content_dict = {
        'ok': True,
        'result': result_dict,
    }
    return stub(status_code=200, ok=True, content=json.dumps(content_dict).encode('utf8'))

def generatestub_requests_get_response_error(error_code:int, description:str):
    content_dict = {
        'ok': False,
        'error_code': error_code,
        'description': description,
    }
    return stub(status_code=error_code, ok=True, content=json.dumps(content_dict).encode('utf8'))
