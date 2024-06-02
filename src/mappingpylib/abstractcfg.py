#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import Dict, List
# data processing
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
# utils
from abc import ABC, abstractmethod
from functools import reduce  # forward compatibility for Python 3
import operator
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

class AbstractCfg(ABC):
    def __init__(self, filepath:str) -> None:
        self._config_filepath = filepath

    @staticmethod
    def _get_value(cfg_dict:Dict, key_list:List[str], fallback=None):
        """Get nested TOML parameter by key list"""

        try:
            result = reduce(operator.getitem, key_list, cfg_dict)
        except Exception:
            if fallback is not None:
                log.info(f"Optional parameter '{key_list}' missing in configuration. Using default:'{fallback}'")
                result = fallback
            else:
                log.error(f"Mandatory parameter missing in configuration:'{key_list}'")
                raise KeyError
        return result

    @staticmethod
    def _get_array(cfg_dict:Dict, key_list:List[str]):
        """Get nested TOML array as python list"""

        try:
            result = reduce(operator.getitem, key_list, cfg_dict)
            if not isinstance(result, list):
                raise KeyError
        except Exception:
            log.error(f"Mandatory parameter array missing in configuration:'{key_list}")
            raise KeyError
        return result

    def _load_file(self) -> Dict:
        toml_dict = None
        # load parameter from toml file
        try:
            with open(self._config_filepath, "rb") as f:
                toml_dict = tomllib.load(f)
        except tomllib.TOMLDecodeError:
            log.error("config.toml can't be decoded. Check syntax.")
        except FileNotFoundError:
            log.error(f"Can't find file '{self._config_filepath}'. Check, if file exists.")
        except Exception:
            log.exception("Unexpected exception at loading config.toml")
        if not isinstance(toml_dict, dict):
            log.error("load(): loading cfg failed")
            raise KeyError
        return toml_dict

    @abstractmethod
    def load(self) -> None:
        # here implement your project pecific config toml file processing
        # example:
        # cfg_dict = self._load_file()
        # self.config_param1 = Cfg._get_value(cfg_dict, ["general","config_param1"], fallback=10)
        pass
