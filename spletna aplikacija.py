#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

# Datoteka, v kateri je baza
baza_datoteka = "fakebook.sqlite"

# Mapa s statičnimi datotekami
static_dir = "./static"





######################################################################
# Funkcije, ki obdelajo zahteve odjemalcev.

@route("/static/<filename:path>")
def static(filename):
    """Splošna funkcija, ki servira vse statične datoteke iz naslova
       /static/..."""
    return static_file(filename, root=static_dir)

@get('/')
def index():
    return template('firstpage.html')

@get("/hero/")
def hero_get():
    """Prikaži formo za hero."""
    cur.execute("SELECT * FROM hero")
    return template("heros.html",heroji = cur)

@get("/cards/")
def cards_get():
    """Prikaži formo za hero."""
    cur.execute("SELECT * FROM karte")
    return template("karte.html",karte = cur)

@get("/deck/")
def deck_get():
    """Prikaži formo za hero."""
    cur.execute("SELECT * FROM deck")
    return template("deck.html",deck = cur)




######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8081)
