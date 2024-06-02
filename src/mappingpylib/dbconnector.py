#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
from typing import Dict, List
# MYSQL database connection
import mysql.connector
#from mysql.connector import Error
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
# Class: DbConnector
#****************************************
class DbConnector():
    def __init__(self, host:str, db_name:str, username:str, password:str, port:int = 3306) -> None:
        self._db_connection: mysql.connector.MySQLConnection = None
        self._host = host
        self._port = port
        self._db_name = db_name
        self._username = username
        self._password = password

    def __del__(self) -> None:
        log.debug("DbConnector: __del__")
        self._disconnect()

    def _connect(self) -> mysql.connector.MySQLConnection:
        """Connect to database, if not already connected"""
        try:
            # only create new connection, if not already a connection is available
            if self._db_connection is None or not self._db_connection.is_connected():
                self._db_connection = mysql.connector.connect(
                    host = self._host,
                    port = self._port,
                    user = self._username,
                    passwd = self._password,
                    database = self._db_name
                )
                log.debug("DbConnector: SQL db connected successfully")
        except Exception:
            log.error("DbConnector: SQL connection error.")
            log.exception("Exception info:")
        return self._db_connection

    def _disconnect(self) -> None:
        """Disconnect a open database connection"""
        if self._db_connection is not None:
            log.debug("DbConnector: disconnect")
            self._db_connection.close()

    def execute_query(self, query:str, commit:bool=False, disconnect:bool=True) -> List[Dict]:
        """Execute a SQL query including connect and disconnect"""
        result = None
        try:
            connection = self._connect()
            cursor = connection.cursor(dictionary=True)
            log.debug(f"DbConnector: SQL query '{query}'...")
            cursor.execute(query)
            if commit:
                result = connection.commit()
            else:
                result = cursor.fetchall()
            cursor.close()
            if disconnect:
                self._disconnect()
            log.debug(f"DbConnector: SQL query executed, result: {result}")
        #except mysql.connector.errors.DatabaseError:
        #    log.error("DbConnector: mySQL DatabaseError. Cound not connect to database. MySQL server down?")
        #    log.exception("Exception info:")
        #    self._disconnect()
        except Exception as error:
            log.error(f"DbConnector: SQL query error: '{error}'")
            self._disconnect()
            result = None
        return result
