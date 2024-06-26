#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
# json handling
import json
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

#****************************************
# Class: PogoTranslation
#****************************************
class PogoTranslation():
    def __init__(self, language:str):
        self._pogodata_json = {}
        self._url = f"https://raw.githubusercontent.com/WatWowMap/pogo-translations/master/static/locales/{language}.json"

    def _get_name_by_id(self, search_name_pre:str, id_num:int, search_name_post:str="") -> str:
        """search and get a dict entry value for given key.
        Following key string is searched with {search_name_pre}{id_num}{search_name_post}.
        """

        name = None
        if isinstance(self._pogodata_json, dict):
            try:
                #find pokemon
                dict_key = f"{search_name_pre}{id_num}{search_name_post}"
                if dict_key in self._pogodata_json.keys():
                    name = self._pogodata_json[dict_key]
                    log.debug(f"name found: {search_name_pre}{id_num}{search_name_post}='{name}'")
            except Exception:
                log.exception("Exception in _get_name_by_id()")
        return name

    def update(self) -> None:
        """update pogodata translation json from external url"""

        try:
            request_response = requests.get(self._url)
            if request_response.ok:
                decoded_response = request_response.content.decode("utf8")
                self._pogodata_json = json.loads(decoded_response)
                log.info("updated pogo translation data successful")
        except Exception:
            log.exception("Exception in update_data()")

    def get_pokemon_name(self, pokemon_id:int) -> str:
        """Return translated pokemon name string for given pokemon_id"""

        name = self._get_name_by_id("poke_", pokemon_id)
        if name is None:
            name = f"Pokemon {pokemon_id}"
        return name

    def get_move_name(self, move_id:int) -> str:
        """Return translated move name string for given move_id"""

        name = self._get_name_by_id("move_", move_id)
        if name is None:
            name = f"Move {move_id}"
        return name

    def get_raidlevel_name(self, raidlevel:int, plural:bool=False) -> str:
        """Return translated raid level name string for given raidlevel (in plural version, if plural=True)"""

        if plural:
            name = self._get_name_by_id("raid_", raidlevel, "_plural")
        else:
            name = self._get_name_by_id("raid_", raidlevel)
        if name is None:
            name = f"{raidlevel}* Raid"
        return name
