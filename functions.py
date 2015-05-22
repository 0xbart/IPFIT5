"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz
"""
import sqlite3
import hashlib

def getHash(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()


def checkLogin(username, password):
    db = sqlite3.connect("db/pythronic.db")
    cursor = db.cursor()
    x = cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE name = '" + username + "'\
                        AND pass = '" + getHash(password) + "');")

    if x.fetchone()[0] == 1:
        return False
    else:
        return True
