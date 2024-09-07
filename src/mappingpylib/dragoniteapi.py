#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import Dict
# logging
import logging
#import mappingpylib
from . import apiconnector
from .apiconnector import ApiConnector

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
#****************************************
# Class: DragoniteApi
#****************************************
class DragoniteApi():
    def __init__(self, hosturl:str, port:int = None, basicauth_dict:Dict[str,str] = None) -> None:
        # Note: dragonite API don't support secret -> skip
        self._api_connector = ApiConnector(hosturl, port)
        if basicauth_dict is not None:
            self._api_connector.set_basicauth(basicauth_dict)

    def get_status(self) -> Dict:
        status_dict = {}
        try:
            status_dict = self._api_connector.get_json("/status/")
        except apiconnector.ApiCommunicationError as error:
            log.error(f"API communication error: {error}")
        except Exception as error:
            log.exception(f"Unexpectd exception: '{error}'")
        return status_dict

    def reload(self) -> bool:
        success = False
        try:
            success = self._api_connector.get_nodata("/reload/")
        except Exception as error:
            log.exception(f"Unexpectd exception: '{error}'")
        return success

    def reload_accounts(self) -> bool:
        success = False
        try:
            success = self._api_connector.get_nodata("/reload/accounts")
        except Exception as error:
            log.exception(f"Unexpectd exception: '{error}'")
        return success