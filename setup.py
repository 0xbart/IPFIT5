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

def createDatabase():
    db = None
    try:
        db = sqlite3.connect("db/pythronic.db")
        createDBTables(db)
        createDBUser(db)
    except e:
        print (" [ERROR] Database couldn't created succesfully.")
    finally:
        if db:
            db.close()


def createDBTables(db):
    cursor = db.cursor()
    sql = ('''CREATE TABLE users (id INTEGER PRIMARY KEY,
              name TEXT, pass TEXT, deleted INTEGER);
              CREATE TABLE logs (id INTEGER PRIMARY KEY,
              datetime TIMESTAMP, description TEXT);
              CREATE TABLE cases (id INTEGER PRIMARY KEY,
              name TEXT, description TEXT, owner TEXT,
              created_at TIMESTAMP, deleted INTEGER)''')
    db.executescript(sql)
    print (" [INFO]: Tables `users`, `logs`, `cases` created succesfully.\n")


def createDBUser(db):
    username = functions.askInput("Enter username", "s")
    password = functions.askInput("Enter password", "s")

    cursor = db.cursor()
    cursor.execute('''INSERT INTO users (name, pass, deleted) VALUES (?,?,?)''',
                      (username, functions.getHash(password), '0'))
    db.commit()


if __name__ == '__main__':
    print ("[ERROR]: setup.py can only be opened by pythronic.py.")
