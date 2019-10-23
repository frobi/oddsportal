#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:50:57 2018

Handle SQLite Database
"""

import sqlite3 as lite
from sqlite3 import Error

# in each module
import logging
logger = logging.getLogger(__name__)

def create_conection(db_name):
    '''
    connect to an existed sqlite db
    '''
    try:
        con = lite.connect(db_name)
        return con
    
    except Error as e:
        print(e)
        logger.error('can not create connection to database %s', db_name)
        
    return None # ?

def chk_tabe(con, table_name):
    '''
    check if table table_name exists
    if not then create it
    '''
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'"
    if not con.execute(tb_exists).fetchone():
        logger.info('table not exists: %s', table_name)
        tb_create = "CREATE TABLE " + table_name + " (\
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,\
                    url        TEXT,\
                    match_date TEXT,\
                    match_hour TEXT,\
                    team_home  TEXT,\
                    team_away  TEXT,\
                    score      TEXT,\
                    odds_home  REAL,\
                    odds_draw  REAL,\
                    odds_away  REAL,\
                    bet_result INTEGER)"
        con.execute(tb_create)
        logger.info('table %s created', table_name)

def insert_oddsportal(con, table_name, data):
    '''
    insert into the oddsportal table
    '''
    sql = "INSERT INTO " + table_name + " (url,match_date,match_hour,team_home,team_away,score,odds_home,odds_draw,odds_away,bet_result) VALUES (?,?,?,?,?,?,?,?,?,?)"
    
    try:
        c = con.cursor()
        c.execute(sql, data)
    except Exception as e:
        logger.warning('insert exception - %s: %s', e, sql)
    #return c.lastrowid

def insert_oddsp_soccer(con, data):
    '''
    insert into the soccer table
    '''
    sql = "INSERT INTO oddsp_soccer (url,match_date,match_hour,teams,score,odds_home,odds_draw,odds_away,bet_result,bet_tot) VALUES (?,?,?,?,?,?,?,?,?,?)"
    
    c = con.cursor()
    c.execute(sql, data)
    #return c.lastrowid

def test_connection(con):
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    return cur.fetchone()