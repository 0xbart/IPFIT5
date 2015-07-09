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
import sys
import time
import setup
import signal
import sqlite3
import hashlib


def getHash(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()


def filehash(filepath):
    md5Hash = None

    try:
        blocksize = 64*1024
        md5 = hashlib.md5()
        with open(filepath, 'rb') as fp:
            while True:
                data = fp.read(blocksize)
                if not data:
                    break
                md5.update(data)
        md5Hash = md5.hexdigest()
    except:
        pass

    return md5Hash


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
            try:
                var = raw_input(" " + message + ": ")

                # Send q or h back for help or quit function!
                if var == 'q' or var == 'h' or var == 'b':
                    break

                var = int(var)
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
        print ' [ERROR]: Connection with the database failed.'

    return result


def createUser(username, password):
    result = False
    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO users (name, pass, deleted)
            VALUES (?,?,?)''', (username, getHash(password), '0'))
        db.commit()
        result = True
    except:
        pass
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


def getUsers():
    users = None

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        rows = cursor.execute("SELECT id, name FROM users \
                               WHERE deleted = '0'")
        users = rows.fetchall()
    except:
        print ' [Error]: while getting users of database.'

    return users


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


def getUserID(name):
    userID = None

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        user = cursor.execute("SELECT id FROM users \
                               WHERE name = '" + name + "'")
        userID = user.fetchone()[0]
    except:
        print ' [Error]: Error while getting the user ID.'

    return userID


def getUsername(ID):
    username = None

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        user = cursor.execute("SELECT name FROM users \
                               WHERE id = '" + ID + "'")
        username = user.fetchone()[0]
    except:
        print ' [Error]: Error while getting the username.'

    return str(username)


def checkUserExist(name):
    existing = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        countRows = cursor.execute("SELECT EXISTS(SELECT 1 FROM users \
                                    WHERE name = '" + name + "');")

        if countRows.fetchone()[0] == 1:
            existing = True
    except:
        return False

    return existing


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


def getUserIDs():
    userIDs = []

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        ids = cursor.execute("SELECT id FROM users \
                                WHERE deleted = '0'")
        ids = ids.fetchall()
        for i in ids:
            userIDs.append(i[0])
    except:
        print ' [ERROR]: Error while getting the user ID\'s'

    return userIDs


def createCase(name, desc, user):
    result = False

    try:
        if not checkCaseExist(name):
            db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
            cursor = db.cursor()
            cursor.execute('''INSERT INTO cases (name, description, owner, created_at, deleted)
                              VALUES (?,?,?,?,?)''', (
                              name, desc, user,
                              time.strftime("%Y-%m-%d"), '0'))
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
            cursor.execute("UPDATE cases SET deleted = '1' \
                            WHERE id = '" + ID + "'")

        if operation == 'p':
            cursor.execute("DELETE FROM cases WHERE id = '" + ID + "'")
            setup.removeCaseDatabase(ID)

        db.commit()
        result = True
    except:
        print '\n [ERROR]: Case cannot be deleted!\n'

    return result


def deleteUser(ID, operation):
    result = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()

        if operation == 'y':
            cursor.execute("UPDATE users SET deleted = '1' \
                            WHERE id = '" + ID + "'")

        if operation == 'p':
            cursor.execute("DELETE FROM users WHERE id = '" + ID + "'")

        db.commit()
        result = True
    except:
        print '\n [ERROR]: user cannot be deleted!\n'

    return result


def createEvidence(name, desc, casename, evidenceType):
    result = False

    try:
        if not checkEvidenceExist(name, casename):
            database = ('db' + getOsSlash() + 'cases' +
                        getOsSlash() + casename + '.db')
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute('''INSERT INTO evidences (name, description, type,
                              created_at, deleted) VALUES (?,?,?,?,?)''', (
                              name, desc, evidenceType,
                              time.strftime("%Y-%m-%d"), '0'))
            db.commit()
            if setup.createEvidenceTables(name, casename, evidenceType):
                result = True
        else:
            print '\n [ERROR]: Name evidence must be unique.\n'
    except:
        print '\n [ERROR]: evidence cannot be created!\n'

    return result


def checkEvidenceExist(name, casename):
    existing = False

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')
        db = sqlite3.connect(database)
        cursor = db.cursor()
        countRows = cursor.execute("SELECT EXISTS(SELECT 1 FROM evidences \
                                    WHERE name = '" + name + "');")

        if countRows.fetchone()[0] == 1:
            existing = True
    except:
        return False

    return existing


def getEvidences(casename):
    evidences = None

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')
        db = sqlite3.connect(database)
        cursor = db.cursor()
        rows = cursor.execute("SELECT id, name FROM evidences \
                               WHERE deleted = '0'")
        rows = rows.fetchall()
        evidences = rows
    except:
        print ' [Error]: while getting evidences of database.'

    return evidences


def getEvidenceIDs(casename):
    evidenceIDs = []

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')
        db = sqlite3.connect(database)
        cursor = db.cursor()
        ids = cursor.execute("SELECT id FROM evidences \
                                WHERE deleted = '0'")
        ids = ids.fetchall()
        for i in ids:
            evidenceIDs.append(i[0])
    except:
        print ' [ERROR]: Error while getting the evidence ID\'s'

    return evidenceIDs


def getEvidence(casename, ID):
    evidenceName = None

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')
        db = sqlite3.connect(database)
        cursor = db.cursor()
        evicence = cursor.execute("SELECT name FROM evidences \
                               WHERE id = '" + ID + "'")
        evidenceName = evicence.fetchone()[0]
    except:
        print ' [Error]: Error while getting the evidence name.'

    return str(evidenceName)


def getEvidenceType(casename, ID):
    eType = None

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')
        db = sqlite3.connect(database)
        cursor = db.cursor()
        evidence = cursor.execute("SELECT type FROM evidences \
                               WHERE id = '" + ID + "'")
        eType = evidence.fetchone()[0]
    except:
        print ' [Error]: Error while getting the evidence type.'

    return str(eType)


def deleteEvidence(casename, ID, operation):
    result = False

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')

        if operation == 'y':
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute("UPDATE evidences SET deleted = '1' \
                            WHERE id = '" + ID + "'")
            db.commit()

        if operation == 'p':
            Etype = getEvidenceType(casename, ID)
            name = getEvidence(casename, ID)

            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute("DELETE FROM evidences WHERE id = '" + ID + "'")
            db.commit()

            setup.deleteEvidence(casename, name, Etype)

        result = True
    except:
        print '\n [ERROR]: evidence cannot be deleted!\n'

    return result


def appendLog(level, message):
    result = False

    try:
        db = sqlite3.connect('db' + getOsSlash() + 'pythronic.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO logs (ddate, datetime, level, description)
                          VALUES (?,?,?,?)''', (
                          time.strftime("%Y-%m-%d"),
                          time.strftime("%Y-%m-%d %H:%M:%S"), level, message))
        db.commit()
        result = True
    except:
        print '\n [ERROR]: Log entry cannot be writed into the database.'

    return result


def appendCaseLog(casename, level, message):
    result = False

    try:
        database = ('db' + getOsSlash() + 'cases' +
                    getOsSlash() + casename + '.db')
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute('''INSERT INTO logs (ddate, datetime, level, description)
                          VALUES (?,?,?,?)''', (
                          time.strftime("%Y-%m-%d"),
                          time.strftime("%Y-%m-%d %H:%M:%S"), level, message))
        db.commit()
        result = True
    except:
        print '\n [ERROR]: Log entry cannot be writed into the database.'

    return result


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    print ' [ERROR]: functions.py can only be opened by pythronic.py.'
