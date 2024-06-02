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
#import code under test
from mappingpylib.pogotranslation import PogoTranslation

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
class Test_pogotranslation(unittest.TestCase):
    def test_de(self):
        testpogotranslation = PogoTranslation("de")
        testpogotranslation.update()
        pokemon_name_str = testpogotranslation.get_pokemon_name(1)
        self.assertEqual("Bisasam", pokemon_name_str)
        move_name_str = testpogotranslation.get_move_name(1)
        self.assertEqual("Donnerschock", move_name_str)
        raidlevel_name_str = testpogotranslation.get_raidlevel_name(1, plural=False)
        self.assertEqual("1 Stern Raid", raidlevel_name_str)
        raidlevel_name_str = testpogotranslation.get_raidlevel_name(1, plural=True)
        self.assertEqual("1 Stern Raids", raidlevel_name_str)

    def test_en(self):
        testpogotranslation = PogoTranslation("en")
        testpogotranslation.update()
        pokemon_name_str = testpogotranslation.get_pokemon_name(1)
        self.assertEqual("Bulbasaur", pokemon_name_str)
        move_name_str = testpogotranslation.get_move_name(1)
        self.assertEqual("Thunder Shock", move_name_str)
        raidlevel_name_str = testpogotranslation.get_raidlevel_name(1, plural=False)
        self.assertEqual("1 Star Raid", raidlevel_name_str)
        raidlevel_name_str = testpogotranslation.get_raidlevel_name(1, plural=True)
        self.assertEqual("1 Star Raids", raidlevel_name_str)

    def test_unknown(self):
        testpogotranslation = PogoTranslation("de")
        testpogotranslation.update()
        pokemon_name_str = testpogotranslation.get_pokemon_name(99999)
        self.assertEqual("Pokemon 99999", pokemon_name_str)
        move_name_str = testpogotranslation.get_move_name(99999)
        self.assertEqual("Move 99999", move_name_str)
        raidlevel_name_str = testpogotranslation.get_raidlevel_name(999, plural=False)
        self.assertEqual("999* Raid", raidlevel_name_str)
        raidlevel_name_str = testpogotranslation.get_raidlevel_name(999, plural=True)
        self.assertEqual("999* Raid", raidlevel_name_str)

'''
****************************************
* Public functions
****************************************
'''
