"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz

    SETUP ONLY SCRIPT
"""
import sqlite3
import hashlib

def createDatabase():
    db = sqlite3.connect("db/pythronic.db")

    createDBTables(db)
    createDBUser(db)

    db.close()


def createDBTables(db):
    cursor = db.cursor()
    sql = ('''CREATE TABLE users (id INTEGER PRIMARY KEY,
              name TEXT, pass TEXT, deleted INTEGER);
              CREATE TABLE logs (id INTEGER PRIMARY KEY,
              datetime TIMESTAMP, description TEXT)''')
    db.executescript(sql)
    print (" [INFO]: Tables `users` and `logs` created succesfully.\n")


def createDBUser(db):
    username = input(" Username: ")
    password = input(" Password: ")

    cursor = db.cursor()
    cursor.execute('''INSERT INTO users (name, pass, deleted) VALUES (?,?,?)''',
                      (username, hashlib.md5(password.encode('utf-8')).hexdigest(), '0'))
    db.commit()
