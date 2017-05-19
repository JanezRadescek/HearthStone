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

with open('CSV1.csv', 'r') as f:
    csvfile = csv.reader(f)
    i = 0
    for row in csvfile:
        if i != 0 and row != []:
            slovar[row[1]] = ""
        i += 1

for key in slovar:
    cur.execute("INSERT INTO hero (ime) VALUES (%s);", [key])
