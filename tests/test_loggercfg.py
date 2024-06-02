#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
#general imports for testcode
#import sys
import io
import logging
#unittest imports
import unittest
from unittest.mock import patch
import misc
#import code under test
from mappingpylib import loggercfg

'''
****************************************
* Global variables
****************************************
'''
log = logging.getLogger(__name__)
tmp_logfile = "./tests/.test_logfile.log"

'''
****************************************
* Classes
****************************************
'''
class Test_is_valid_loglevel(unittest.TestCase):
    def test_is_valid_loglevel_debug(self):
        self.assertTrue(loggercfg.is_valid_loglevel("DEBUG"))
    def test_is_valid_loglevel_info(self):
        self.assertTrue(loggercfg.is_valid_loglevel("INFO"))
    def test_is_valid_loglevel_warning(self):
        self.assertTrue(loggercfg.is_valid_loglevel("WARNING"))
    def test_is_valid_loglevel_error(self):
        self.assertTrue(loggercfg.is_valid_loglevel("ERROR"))
    def test_is_valid_loglevel_invalid(self):
        self.assertFalse(loggercfg.is_valid_loglevel("INVALID_LEVEL"))
    def test_is_valid_loglevel_wrong_type(self):
        self.assertFalse(loggercfg.is_valid_loglevel(123))

class Test_config_logger(unittest.TestCase):
    def setUp(self):
        misc.delete_file_if_exist(tmp_logfile)

    @patch('sys.stderr', new_callable = io.StringIO)
    @patch('sys.stdout', new_callable = io.StringIO)
    def test_config_logger_default(self, mock_stdout, mock_stderr):
        test_logger = logging.getLogger("test_default")
        loggercfg.config_logger(test_logger)
        # debug msg
        test_logger.debug("debug message")
        self.assertEqual("", mock_stdout.getvalue())
        self.assertEqual("", mock_stderr.getvalue())
        # info msg
        clear_stream_mocks(mock_stdout, mock_stderr)
        extected_out = "[   INFO] info message\n"
        test_logger.info("info message")
        self.assertIn(extected_out, mock_stdout.getvalue())
        self.assertEqual("", mock_stderr.getvalue())
        # warning msg
        clear_stream_mocks(mock_stdout, mock_stderr)
        extected_out = "[WARNING] warning message\n"
        test_logger.warning("warning message")
        self.assertIn(extected_out, mock_stdout.getvalue())
        self.assertEqual("", mock_stderr.getvalue())
        # error msg
        clear_stream_mocks(mock_stdout, mock_stderr)
        extected_out = "[  ERROR] error message\n"
        test_logger.error("error message")
        self.assertEqual("", mock_stdout.getvalue())
        self.assertIn(extected_out, mock_stderr.getvalue())

    @patch('sys.stderr', new_callable = io.StringIO)
    @patch('sys.stdout', new_callable = io.StringIO)
    def test_config_logger_file_warning(self, mock_stdout, mock_stderr):
        test_logger = logging.getLogger("test_file_warning")
        loggercfg.config_logger(test_logger, console_loglevel = "DEBUG", file_loglevel = "WARNING", file_name = tmp_logfile)
        # debug msg
        extected_out = "[  DEBUG] debug message\n"
        test_logger.debug("debug message")
        self.assertIn(extected_out, mock_stdout.getvalue())
        self.assertEqual("", mock_stderr.getvalue())
        # info msg
        clear_stream_mocks(mock_stdout, mock_stderr)
        extected_out = "[   INFO] info message\n"
        test_logger.info("info message")
        self.assertIn(extected_out, mock_stdout.getvalue())
        self.assertEqual("", mock_stderr.getvalue())
        # warning msg
        clear_stream_mocks(mock_stdout, mock_stderr)
        extected_out = "[WARNING] warning message\n"
        test_logger.warning("warning message")
        self.assertIn(extected_out, mock_stdout.getvalue())
        self.assertEqual("", mock_stderr.getvalue())
        # error msg
        clear_stream_mocks(mock_stdout, mock_stderr)
        extected_out = "[  ERROR] error message\n"
        test_logger.error("error message")
        self.assertEqual("", mock_stdout.getvalue())
        self.assertIn(extected_out, mock_stderr.getvalue())

    def test_config_logger_wrong_input_type(self):
        test_logger = logging.getLogger("Test_config_logger")
        with self.assertRaises(TypeError):
            loggercfg.config_logger(test_logger, 1)

    def test_config_logger_wrong_loglevel(self):
        test_logger = logging.getLogger("Test_config_logger")
        with self.assertRaises(ValueError):
            loggercfg.config_logger(test_logger, "blub")

'''
****************************************
* Public functions
****************************************
'''
def clear_stream_mocks(mock_stdout:io.StringIO, mock_stderr:io.StringIO) -> None:
    mock_stdout.truncate(0)
    mock_stdout.seek(0)
    mock_stderr.truncate(0)
    mock_stderr.seek(0)