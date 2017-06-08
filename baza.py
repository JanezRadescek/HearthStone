#!/usr/bin/python
# -*- encoding: utf-8 -*-
 
from bottle import *
import auth
import csv
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki



######################################################################

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogocimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
slovar = {}

##with open('CSV1.csv', 'r') as f:
##    csvfile = csv.reader(f)
##    i = 0
##    for row in csvfile:
##        if i != 0 and row != []:
##            slovar[row[1]] = ""
##        i += 1
##
##for key in slovar:
##    cur.execute("INSERT INTO hero (ime) VALUES (%s);", [key])


heros = {}
heros["druid"] = 11
heros["hunter"] = 16
heros["mage"] = 12
heros["paladin"] = 10
heros["priest"] = 9
heros["rogue"] = 15
heros["shaman"] = 14
heros["warlock"] = 13
heros["warrior"] = 9
heros["vsi"] = 17



with open('pureHTML2_karte.csv', 'r') as f:
    csvfile = csv.reader(f,delimiter =';')
    for row in csvfile:
        cur.execute("INSERT INTO karte (ime,expansion,rarity,mana_cost,class) VALUES (%s,%s,%s,%s,%s);", [row[0],int(row[1]),int(row[2]),int(row[3]),heros[row[4]]])







        
