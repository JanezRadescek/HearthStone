#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2
from psycopg2 import IntegrityError
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

# Datoteka, v kateri je baza

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
    """Prikaži formo za karte."""
    #cur.execute("SELECT * FROM karte")
    cur.execute("Select * from karte Join hero on hero.id = karte.class ;")
    return template("karte.html",karte = cur)

@get("/deck/")
def deck_get():
    """Prikaži formo za deck."""
    if 'id' in request.GET.keys():
        kateri = request.GET['id']
        cur.execute("Select * from jevdecku Join karte on karta =karte.id Join hero on hero.id = karte.class WHERE deck = (%s);", [kateri])
        return template("jevdecku.html",jevdecku = cur)
    else:
        cur.execute("SELECT * FROM deck")
        return template("deck.html",deck = cur)

@get("/createdeck/")
def create():
    """Prikaži formo za naredit deck."""
    if 'hero' in request.GET.keys():
        hero = request.GET['hero']
        hero = hero.lower()
        cur.execute("Select * from karte Join hero on hero.id = karte.class where hero.ime = (%s) or hero.ime = (%s) ORDER BY karte.ime ASC;",[hero,'vsi'])
        return template("createdeck.html",create = cur,heroj = hero)
    else:
        cur.execute("Select * from hero")
        return template("createdeck1.html",create = cur,napaka = None)


@post("/createdeck/")
def create():
    """Prikaži formo za naredit deck."""
    ime = request.POST['ime']
    avtor = request.POST['avtor']
    try:
        if ime != "" and avtor != "":
            cur.execute("INSERT INTO deck (ime,avtor) VALUES ((%s),(%s));",[ime,avtor])
            cur.execute("SELECT id from deck where ime =(%s) and avtor = (%s);",[ime,avtor])
            a = cur.fetchone()
            pozicija = int(a[0])
            for el in request.POST:
                if el == "ime" or el == "avtor":
                    pass
                else:
                    indeks = int(el)
                    vrednost = request.POST[el]
                    if vrednost != "":
                        vrednost = int(vrednost)
                        cur.execute("INSERT INTO jevdecku (karta,deck,stevilo) VALUES ((%s),(%s),(%s));",[indeks,pozicija,vrednost])
            return template("deck.html",deck = cur)
        else:
            cur.execute("Select * from hero")
            return template("createdeck1.html",create = cur,napaka = "You must enter a name.")
        
    except IntegrityError:
        cur.execute("Select * from hero")
        return template("createdeck1.html",create = cur,napaka = "Deck name already exists.")

######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
