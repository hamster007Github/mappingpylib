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
# Class: RotomApi
#****************************************
class RotomApi():
    def __init__(self, hosturl:str, port:int = None, basicauth_dict:Dict[str,str] = None, secretauth:str = None) -> None:
        self._api_connector = ApiConnector(hosturl, port)
        if basicauth_dict is not None:
            self._api_connector.set_basicauth(basicauth_dict)
        elif secretauth is not None:
            secretauth_dict = {"x-rotom-secret": secretauth}
            self._api_connector.set_secretcauth(secretauth_dict)

    def _get_worker_from_device(self, workers_dict, device_id:str):
        worker_list = []
        if workers_dict:
            for worker in workers_dict:
                if device_id == worker["deviceId"]:
                    worker_list.append(worker["worker"])
        return worker_list

    def get_status(self) -> dict:
        '''
        get raw status dict from /api/status. Return 'None' in case of error
        '''
        status_dict = None
        try:
            status_dict = self._api_connector.get_json("/api/status")
        except apiconnector.ApiCommunicationError as error:
            log.error(f"API communication error: {error}")
        except Exception as error:
            log.exception(f"Unexpectd exception: '{error}'")
        return status_dict

    def get_status_devicelist(self) -> dict:
        '''
        get custom device status list. Return 'None' in case of error
        '''
        devicestatus_list = None
        try:
            status_dict = self.get_status()
            devicestatus_list = []
            log.debug(f"received status_dict: {status_dict}")
            if status_dict is not None:
                devices = status_dict["devices"]
                workers = status_dict["workers"]
                for device in devices:
                    device_info = {
                        "name":     device["deviceId"],
                        "isAlive":  device["isAlive"],
                        "version":  device["version"],
                        "lastseen": int(device["dateLastMessageReceived"] / 1000),
                        "workers":  []
                    }
                    #get all worker for this device
                    worker_list = self._get_worker_from_device(workers, device["deviceId"])
                    if worker_list:
                        for worker in worker_list:
                            worker_info = {
                                "name":     worker["workerId"],
                                "isAlive":  worker["isAlive"],
                                "version":  worker["version"],
                                "lastseen": int(worker["dateLastMessageReceived"] / 1000)
                            }
                            device_info["workers"].append(worker_info)
                    devicestatus_list.append(device_info)
        except Exception as error:
            log.exception(f"Unexpectd exception: '{error}'")
        return devicestatus_list
