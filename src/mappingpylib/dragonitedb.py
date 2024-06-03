#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import Dict, List
# logging
import logging
#mappingpylib
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

#****************************************
# Class: DragoniteDb
#****************************************
class DragoniteDb():
    def __init__(self, host:str, db_name:str, username:str, password:str, port:int = 3306) -> None:
        """ """
        self._dbconnector = DbConnector(
                host = host,
                port = port,
                db_name = db_name,
                username = username,
                password = password
        )

    def __del__(self):
        del self._dbconnector

    def get_device_status(self) -> List[Dict]:
        """Get device status values.
        
        Following dict values will be returned for each device:
         - ["name]: device uuid
         - ["mode"]: assigned instance type
         - ["instance_name"]: assigned instance name
         - ["lastseen_local"]: timestamp of last received proto data (aka last_seen) in local time (Dragonite default)
        """
        return None

    def get_account_number(self, min_level:int=None, max_level:int=None, is_invalid:bool=None, is_disabled:bool=None, is_warned:bool=None, is_suspended:bool=None, is_banned:bool=None, has_cooldown:bool=None, has_valid_token:bool=None) -> int:
        """Number accounts matching with filters by optional parameter."""
        count = None
        try:
            # build filter query
            filter_query_list = []
            if min_level is not None:
                filter_query_list.append(f"level >= {min_level}")
            if max_level is not None:
                filter_query_list.append(f"level <= {max_level}")
            if is_invalid is not None:
                tmp_str = "invalid"
                if not is_invalid:
                    tmp_str = "NOT " + tmp_str
                filter_query_list.append(tmp_str)
            if is_disabled is not None:
                if is_disabled:
                    tmp_str = "((consecutive_disable_count <= 1 AND (UNIX_TIMESTAMP() - 4*86400) < last_disabled) OR (consecutive_disable_count >= 2 AND (UNIX_TIMESTAMP() - 30*86400) < last_disabled))"
                else:
                    tmp_str = "((consecutive_disable_count <= 1 AND UNIX_TIMESTAMP() - 4*86400 > coalesce(last_disabled, 0)) OR (consecutive_disable_count >= 2 AND UNIX_TIMESTAMP() - 30*86400 > coalesce(last_disabled, 0)))"
                filter_query_list.append(tmp_str)
            if is_warned is not None:
                if is_warned:
                    tmp_str = "(warn_expiration > unix_timestamp())"
                else:
                    tmp_str = "(warn_expiration <= unix_timestamp())"
                filter_query_list.append(tmp_str)
            if is_suspended is not None:
                tmp_str = "suspended"
                if not is_suspended:
                    tmp_str = "NOT " + tmp_str
                filter_query_list.append(tmp_str)
            if is_banned is not None:
                tmp_str = "banned"
                if not is_banned:
                    tmp_str = "NOT " + tmp_str
                filter_query_list.append(tmp_str)
            if has_cooldown is not None:
                if has_cooldown:
                    tmp_str = "(last_selected IS NOT NULL AND last_selected > UNIX_TIMESTAMP() - 169 *3600)"
                else:
                    tmp_str = "(last_selected IS NULL OR last_selected <= UNIX_TIMESTAMP() - 169 *3600)"
                filter_query_list.append(tmp_str)
            if has_valid_token is not None:
                if has_valid_token:
                    tmp_str = "(last_refreshed > (UNIX_TIMESTAMP() - 30*86400) AND refresh_token != '' AND refresh_token IS NOT NULL)"
                else:
                    tmp_str = "(last_refreshed <= (UNIX_TIMESTAMP() - 30*86400) OR refresh_token == '' OR refresh_token IS NULL)"
                filter_query_list.append(tmp_str)
            sql_query = "SELECT count(*) as count FROM account"
            if len(filter_query_list):
                sql_query += " WHERE " + filter_query_list.pop(0)
                for filter_query in filter_query_list:
                    sql_query += f" AND {filter_query}"
            # execute query
            log.debug(f"new get_account_number() query: {sql_query}")
            count = self._dbconnector.execute_query(sql_query)[0]["count"]
        except Exception as error:
            log.error(f"get_account_number(): unexpected exception: '{error}'")
        return count