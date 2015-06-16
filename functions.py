"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz
"""
import time
import sqlite3
import hashlib

def getHash(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()


def checkLogin(username, password):
    db = sqlite3.connect("db/pythronic.db")
    cursor = db.cursor()
    countRows = cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE name = '" + username + "'\
                                AND pass = '" + getHash(password) + "');")

    if countRows.fetchone()[0] == 1:
        return False
    else:
        return True


def getCases():
    db = sqlite3.connect("db/pythronic.db")
    cursor = db.cursor()
    cases = cursor.execute("SELECT id, name FROM cases WHERE deleted = '0'")
    return cases.fetchall()


def checkCaseExist(name):
    db = sqlite3.connect("db/pythronic.db")
    cursor = db.cursor()
    countRows = cursor.execute("SELECT EXISTS(SELECT 1 FROM cases WHERE name = '" + name + "');")

    if countRows.fetchone()[0] == 1:
        return True
    else:
        return False


def getCasesNumbers():
    db = sqlite3.connect("db/pythronic.db")
    cursor = db.cursor()
    cases = cursor.execute("SELECT id FROM cases WHERE deleted = '0'")
    return cases.fetchall()


def createCase(name, desc, user):
    if not checkCaseExist(name):
        db = sqlite3.connect("db/pythronic.db")
        cursor = db.cursor()
        cursor.execute('''INSERT INTO cases (name, description, owner, created_at, deleted) VALUES (?,?,?,?,?)''',
                          (name, desc, user, time.strftime("%Y-%m-%d"), '0'))
        db.commit()
    else:
        print ("\n [ERROR]: Name case must be unique.\n")
