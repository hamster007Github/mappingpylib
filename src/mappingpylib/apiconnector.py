#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import Dict
# url handling
import requests
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
class ApiCommunicationError(Exception):
    pass



#****************************************
# Class: ApiConnector
#****************************************
class ApiConnector():
    def __init__(self, hosturl:str, port:int = None) -> None:
        """ ApiConnector constructor
        hosturl: shall beginn with "http://" or "https://"
        """
        if port is not None:
            self._base_url = hosturl + f":{port}"
        else:
            self._base_url = hosturl
        self._hosturl = hosturl
        self._port = port
        self._basicauth = None
        self._secretauth = None

    def _get_request(self, url:str, statuscode_as_exception:bool = True):
        response = None
        request_url = self._base_url + url
        try:
            if self._secretauth is not None:
                response = requests.get(request_url, headers = self._secretauth)
            elif self._basicauth is not None:
                response = requests.get(request_url, auth = self._basicauth)
            else:
                response = requests.get(request_url)
            if statuscode_as_exception:
                response.raise_for_status()
        except requests.exceptions.RequestException as error:
            log.debug(f"_get_request: http-get communication error: {error}")
            raise ApiCommunicationError(f"{error}")
        except Exception as error:
            log.error(f"_get_request: unexpected exception: {error}")
            raise ApiCommunicationError(f"{error}")
        return response

    def _post_request(self, url:str, data=None, json=None):
        response = None
        request_url = self._base_url + url
        try:
            if self._secretauth is not None:
                response = requests.post(request_url, headers = self._secretauth, data = data, json = json)
            elif self._basicauth is not None:
                response = requests.post(request_url, auth = self._basicauth, data = data, json = json)
            else:
                response = requests.post(request_url, data = data, json = json)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            log.debug("_get_request: http-get communication error: {error}")
            raise ApiCommunicationError(f"{error}")
        except Exception as error:
            log.error("_get_request: unexpected exception: {error}")
            raise ApiCommunicationError(f"{error}")
        return response

    def set_basicauth(self, username:str, password:str) -> None:
        # invalidate auth bearer data
        self._secretauth = None
        self._basicauth = requests.auth.HTTPBasicAuth(username, password)

    def set_secretauth(self, secret_name:str, secret:str) -> None:
        # invalidate basic auth data
        self._basicauth = None
        self._secretauth = {secret_name: secret}

    def get_json(self, suburl:str) -> Dict| None:
        """http-get request and return response json
        Note: if response is no JSON compatible, ValueError will be raised
        """
        response_json = None
        try:
            response = self._get_request(suburl)
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            log.error("get_json_data(): error in decoding JSON data. Most likely response not containing JSON data.")
            log.debug(f"get_json_data() response: {response.text}")
            raise ValueError("error in decoding JSON data")
        #except ApiCommunicationError as error:
        #    log.error(f"get_json_data(): communication error '{error}'")
        return response_json

    def get_text(self, suburl:str) -> str | None:
        """http-get request and return response text"""
        response_text = None
        try:
            response = self._get_request(suburl)
            response_text = response.text
        except ApiCommunicationError as error:
            log.error(f"get_text(): communication error '{error}'")
        return response_text

    def get_nodata(self, suburl:str) -> bool:
        """http-get request and return success"""
        response_status = False
        try:
            self._get_request(suburl)
            response_status = True
        except ApiCommunicationError as error:
            log.error(f"get_status(): communication error '{error}'")
        return response_status

    def post_request(self, suburl:str, data=None, json=None) -> None:
        try:
            self._post_request(suburl, data, json)
        except ApiCommunicationError as error:
            log.error(f"post_request(): communication error '{error}'")

