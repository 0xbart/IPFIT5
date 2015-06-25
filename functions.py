"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz

    FUNCTIONS ONLY SCRIPT
"""
from sys import platform as _platform
import time
import sqlite3
import hashlib
import signal
import sys
import setup


def getHash(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()


def askInput(message, type):
    var = None
    while True:
        if type == 's':
            try:
                var = raw_input(" " + message + ": ")
                break
            except:
                print '\n Wrong input, try again. \n'
        elif type == 'i':
            """
            DIT VERBETEREN, CATCH DE Q!

            while True:
            value = raw_input('Value between 0 and 100:')
            try:
               value = int(value)
            except ValueError:
               print 'Valid number, please'
               continue
            if 0 <= value <= 100:
               break
            else:
               print 'Valid range, please: 0-100'

            """
            try:
                var = int(input(' ' + message + ': '))
                break
            except:
                print '\n Wrong input, try again. \n'
        else:
            var = None
            break
    return var


def getOsSlash():
    slash = None

    if _platform == 'linux' or _platform == 'linux2':
        slash = '/'
    elif _platform == 'darwin':
        slash = '/'
    elif _platform == 'win32':
        slash = '\\'

    return slash


#
# ONDERSTAAND ZIJN FUCTIES MET CONNECTIES NAAR DE DATABASE!
#


def checkLogin(username, password):
    result = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        countRows = cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE name = '" + username + "'\
                                    AND pass = '" + getHash(password) + "');")

        if countRows.fetchone()[0] == 1:
            result = True
    except:
        print ' [ERROR]: Connection with the database isn\'t possible at this moment.'

    return result


def getCases():
    cases = None

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        rows = cursor.execute("SELECT id, name FROM cases \
                               WHERE deleted = '0'")
        cases = rows.fetchall()
    except:
        print ' [Error]: while getting cases of database.'

    return cases


def getCaseID(name):
    ID = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        case = cursor.execute("SELECT id FROM cases \
                               WHERE name = '" + name + "'")
        ID = case.fetchone()[0]
    except:
        print ' [Error]: Error while getting the case ID.'

    return ID


def getCaseName(ID):
    name = None

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        case = cursor.execute("SELECT name FROM cases \
                               WHERE id = '" + ID + "'")
        name = case.fetchone()[0]
    except:
        print ' [Error]: Error while getting the case name.'

    return name


def checkCaseExist(name):
    existing = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        countRows = cursor.execute("SELECT EXISTS(SELECT 1 FROM cases \
                                    WHERE name = '" + name + "');")

        if countRows.fetchone()[0] == 1:
            existing = True
    except:
        return False

    return existing


def getCasesNumbers():
    casesNumbers = []

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        cases = cursor.execute("SELECT id FROM cases \
                                WHERE deleted = '0'")
        cases = cases.fetchall()
        for case in cases:
            casesNumbers.append(case[0])
    except:
        print ' [ERROR]: Error while getting the case numbers'

    return casesNumbers


def createCase(name, desc, user):
    result = False

    try:
        if not checkCaseExist(name):
            db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
            cursor = db.cursor()
            cursor.execute('''INSERT INTO cases (name, description, owner, created_at, deleted)
                              VALUES (?,?,?,?,?)''', (
                              name, desc, user, time.strftime("%Y-%m-%d"), '0'))
            db.commit()
            if setup.createCaseDatabase(name, desc):
                result = True
        else:
            print '\n [ERROR]: Name case must be unique.\n'
    except:
        print '\n [ERROR]: Case cannot be created!\n'

    return result


def deleteCase(ID, operation):
    result = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()

        if operation == 'y':
            cursor.execute("UPDATE cases SET deleted = '1' WHERE id = '" + ID + "'")

        if operation == 'p':
            cursor.execute("DELETE FROM cases WHERE id = '" + ID + "'")
            setup.removeCaseDatabase(ID)

        db.commit()
        result = True
    except:
        print '\n [ERROR]: Case cannot be deleted!\n'

    return result


def appendLog(level, message):
    result = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO logs (ddate, datetime, level, description)
                          VALUES (?,?,?,?)''', (
                          time.strftime("%Y-%m-%d"), time.strftime("%Y-%m-%d %H:%M:%S"), level, message))
        db.commit()
        result = True
    except:
        print '\n [ERROR]: Log entry cannot be writed into the database.'

    return result


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    print ' [ERROR]: functions.py can only be opened by pythronic.py.'
