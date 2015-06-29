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
import functions
import os
import time

# START DEFAULT DATABASE


def createDatabase():
    print ' [INFO]: Pythronic setup executed! Please follow instructions.'
    db = None
    try:
        db = sqlite3.connect('db' + functions.getOsSlash() + 'pythronic.db')
        createDBTables(db)
        createDBUser(db)
    except:
        print ' [ERROR] Database couldn\'t created succesfully.'
    finally:
        if db:
            db.close()


def createDBTables(db):
    try:
        cursor = db.cursor()
        sql = ('''CREATE TABLE users (id INTEGER PRIMARY KEY,
                  name TEXT, pass TEXT, deleted INTEGER);
                  CREATE TABLE logs (id INTEGER PRIMARY KEY, ddate DATE,
                  datetime TIMESTAMP, level TEXT, description TEXT);
                  CREATE TABLE cases (id INTEGER PRIMARY KEY,
                  name TEXT, description TEXT, owner TEXT,
                  created_at TIMESTAMP, deleted INTEGER)''')
        db.executescript(sql)
        print ' [INFO]: Tables `users`, `logs`, `cases` created succesfully.\n'
    except:
        print ' [Error]: Tables couldn\'t be created.\n'


def createDBUser(db):
    try:
        username = functions.askInput('Enter username', 's')
        password = functions.askInput('Enter password', 's')

        cursor = db.cursor()
        cursor.execute('''INSERT INTO users (name, pass, deleted)
            VALUES (?,?,?)''', (username, functions.getHash(password), '0'))
        db.commit()
    except:
        print ' [Error]: User cannot be created!'

# END DEFAULT DATABASE
# START CASE DATABASE


def createCaseDatabase(name, description):
    result = False
    db = None
    try:
        db = sqlite3.connect('db' + functions.getOsSlash() + 'cases' +
                             functions.getOsSlash() + name + '.db')
        if createCaseDBTables(db):
            if createCaseDBValue(db, name, description):
                result = True
    except e:
        print ' [ERROR] Database couldn\'t created succesfully.'
    finally:
        if db:
            db.close()
            return result


def createCaseDBTables(db):
    result = False

    try:
        cursor = db.cursor()
        sql = ('''CREATE TABLE general (id INTEGER PRIMARY KEY,
                  name TEXT, description TEXT, created_at TIMESTAMP);
                  CREATE TABLE evidences (id INTEGER PRIMARY KEY, name TEXT,
                  description TEXT, deleted INTEGER);''')
        db.executescript(sql)
        result = True
    except:
        print ' [Error]: Tables couldn\'t be created.\n'

    return result


def createCaseDBValue(db, name, description):
    result = False

    try:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO general (name, description, created_at)
            VALUES (?,?,?)''', (
            name, description, time.strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
        result = True
    except:
        print ' [Error]: Value cannot be created!'

    return result


def removeCaseDatabase(ID):
    result = False
    try:
        name = functions.getCaseName(str(ID))
        os.remove('db' + functions.getOsSlash() + 'cases' +
                  functions.getOsSlash() + name + '.db')
        result = True
    except:
        print ' [ERROR]: database cannot be removed.'

    return result

# END CASE DATABASE


if __name__ == '__main__':
    print ("[ERROR]: setup.py can only be opened by pythronic.py.")
