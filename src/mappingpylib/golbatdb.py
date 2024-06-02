#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import Dict, List, Tuple
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
# Class: GolbatDb
#****************************************
class GolbatDb():
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

    def _calculate_percentage(self, value1:float, value2:float,  digits:int = 0) -> float:
        """Helperfunction to get [count] value from first row of sql query result."""
        result = 0.0
        try:
            result = round((float(value1) / float(value2) * 100.0), digits)
        except ZeroDivisionError:
            log.warning("_calculate_percentage(): divide by 0")
        except Exception:
            log.exception(f"_calculate_percentage(): unexpected exception with value1:{value1} and value_2:{value2}")
        return result

    def get_pokemon_stats(self, timestamp_latest_utc:int, time_window_min:int, disconnect:bool = False) -> Tuple[int, int, float]:
        """get pokemon statistic values
          timestamp_latest_utc: for newest timestamp as latest use 'datetime.now(timezone.utc).timestamp()'

          return (3 values):
            -num all pokemon
            -num pokemon with iv
            -pokemon percentage with iv [0.0 ... 100.0]
        """
        # calculate Golbat dataset timestamp based on timestamp_latest_utc (Golbat always has fix datetime 0, 60, ...)
        timestamp_stats_latest = int((timestamp_latest_utc // 60) * 60)
        timestamp_stats_oldest = int(timestamp_stats_latest - (60 * time_window_min))
        sql_query = f"SELECT sum(totMon) AS mon_all, sum(ivMon) AS mon_iv FROM (SELECT totMon, ivMon FROM pokemon_area_stats WHERE area='world' AND fence='world' AND datetime >= {timestamp_stats_oldest} AND datetime <= {timestamp_stats_latest}) t1;"
        results = self._dbconnector.execute_query(sql_query, disconnect=disconnect)
        mon_all = 0
        mon_iv  = 0
        try:
            if (results is not None) and results:
                mon_all = results[0]["mon_all"]
                mon_iv  = results[0]["mon_iv"]
            else:
                log.debug(f"_get_pokemon_stats(): no 'pokemon_area_stats' table entries found from timestamp {timestamp_stats_oldest} to {timestamp_stats_latest}")
        except Exception:
            log.exception(f"_get_pokemon_stats() exception: sql result:'{results}'")
            mon_all = 0
            mon_iv  = 0
        # check for None and replace with 0
        if mon_all is None:
            mon_all = 0
        if mon_iv is None:
            mon_iv = 0
        iv_percentage = self._calculate_percentage(mon_iv, mon_all)
        return mon_all, mon_iv, iv_percentage

    def get_raids(self, raidlevel_list:List[int], unknown_raids:bool = True, geofence:str = "", order_time_reverse:bool = False) -> List[Dict]:
        """Return active raids from scanner according provided filter. If you don't want to filter raids by geofence, set geofence = ''"""

        sql_order = "DESC" if order_time_reverse else "ASC"
        sql_geofence = "" if geofence == "" else f"AND ST_CONTAINS(st_geomfromtext('POLYGON(({geofence}))') , point(lat,lon))"
        sql_unknown_raids = "" if unknown_raids else "AND raid_pokemon_id <> 0"
        raidlevel_str = ','.join([str(raidlevel) for raidlevel in raidlevel_list])
        sql_query = f"SELECT name AS gym_name, raid_level, raid_pokemon_id, raid_battle_timestamp, raid_end_timestamp, raid_pokemon_move_1 AS atk_fast, raid_pokemon_move_2 AS atk_charge, lat, lon FROM gym WHERE UNIX_TIMESTAMP() < raid_end_timestamp AND raid_level IN ({raidlevel_str}) {sql_geofence} {sql_unknown_raids} ORDER BY raid_end_timestamp {sql_order};"
        dbreturn = self._dbconnector.execute_query(sql_query)
        return dbreturn
