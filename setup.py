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
    while True:
        try:
            username = functions.askInput('Enter username', 's')
            password = functions.askInput('Enter password', 's')
            if len(username) >= 4 and len(password) >= 4:
                hashPassword = functions.getHash(password)
                cursor = db.cursor()
                cursor.execute('''INSERT INTO users (name, pass, deleted)
                    VALUES (?,?,?)''', (username, hashPassword, '0'))
                db.commit()
                break
            else:
                print (' \n [ERROR]: Sorry, choose a name and password '
                       'longer then 3 characters!\n')
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
                  description TEXT, type INTEGER, created_at TIMESTAMP,
                  deleted INTEGER);''')
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
# START EVIDENCE DATABASE


def createEvidenceTables(name, casename, evidenceType):
    result = False

    try:
        db = sqlite3.connect('db' + functions.getOsSlash() + 'cases' +
                             functions.getOsSlash() + casename + '.db')
        cursor = db.cursor()

        if evidenceType == '1':
            sql = [
                'CREATE TABLE `' + name + '_hardware` ('
                'id INTEGER PRIMARY KEY, processor TEXT, '
                'usb_devices TEXT, system_arch TEXT, proc_name TEXT, '
                'proc_family TEXT, used_memory TEXT, free_memory TEXT, '
                'total_memory TEXT)',  # 1
                'CREATE TABLE `' + name + '_software` ('
                'id INTEGER PRIMARY KEY, name TEXT)',  # 2
                'CREATE TABLE `' + name + '_users` ('
                'id INTEGER PRIMARY KEY, name TEXT)',  # 3
                'CREATE TABLE `' + name + '_general` ('
                'id INTEGER PRIMARY KEY, os TEXT, ddate TEXT, '
                'ttime TEXT, timezone TEXT, clip_out TEXT, '
                'pc_name TEXT, username TEXT)',  # 4
                'CREATE TABLE `' + name + '_network` ('
                'id INTEGER PRIMARY KEY, ip TEXT, mac TEXT, '
                'connected_ip TEXT)',  # 5
                'CREATE TABLE `' + name + '_cloud` ('
                'id INTEGER PRIMARY KEY, dropbox INTEGER, '
                'onedrive INTEGER, evernote INTEGER, googledrive INTEGER)',
                'CREATE TABLE `' + name + '_virus` ('
                'id INTEGER PRIMARY KEY, virus_name TEXT, '
                'virus_hash TEXT, virus_output TEXT)',  # 7
                'CREATE TABLE `' + name + '_drive` ('
                'id INTEGER PRIMARY KEY, drive_name TEXT, '
                'drive_mountpoint TEXT, drive_filesystem TEXT)',  # 8
                'CREATE TABLE `' + name + '_files` ('
                'id INTEGER PRIMARY KEY, name TEXT, size TEXT, '
                'shahash TEXT, md5hash TEXT)',  # 9
                'CREATE TABLE `' + name + '_browser` ('
                'id INTEGER PRIMARY KEY, his_chrome TEXT, his_ff TEXT, '
                'his_iexplorer TEXT, his_safari TEXT)',  # 10
                'CREATE TABLE `' + name + '_linux_logon` ('
                'id INTEGER PRIMARY KEY, name TEXT)',  # 11
                'CREATE TABLE `' + name + '_win_logon` ('
                'id INTEGER PRIMARY KEY, name TEXT)',  # 12
                'CREATE TABLE `' + name + '_pslist` ('
                'id INTEGER PRIMARY KEY, name TEXT)',  # 13
                'CREATE TABLE `' + name + '_files_overview` ('
                'id INTEGER PRIMARY KEY, html_view TEXT)'  # 3
            ]

        elif evidenceType == '2':
            sql = [
                'CREATE TABLE `' + name + '_files` ('
                'id INTEGER PRIMARY KEY, name TEXT, size TEXT,'
                ' shahash TEXT, md5hash TEXT)',  # 1
                'CREATE TABLE `' + name + '_virus` ('
                'id INTEGER PRIMARY KEY, virus_name TEXT, '
                'virus_hash TEXT, virus_output TEXT)',  # 2
                'CREATE TABLE `' + name + '_files_overview` ('
                'id INTEGER PRIMARY KEY, html_view TEXT)'  # 3
            ]

        for i in range(len(sql)):
            cursor.execute(sql[i])

        db.commit()
        result = True
    except:
        print ' [Error]: Tables couldn\'t be created.\n'

    return result


def deleteEvidence(casename, name, evidenceType):
    result = False

    try:
        db = sqlite3.connect('db' + functions.getOsSlash() + 'cases' +
                             functions.getOsSlash() + casename + '.db')
        cursor = db.cursor()

        if evidenceType == '1':
            sql = [
                'DROP TABLE `' + name + '_browser`',  # 1
                'DROP TABLE `' + name + '_cloud`',  # 2
                'DROP TABLE `' + name + '_drive`',  # 3
                'DROP TABLE `' + name + '_files`',  # 4
                'DROP TABLE `' + name + '_general`',  # 5
                'DROP TABLE `' + name + '_hardware`',  # 6
                'DROP TABLE `' + name + '_network`',  # 7
                'DROP TABLE `' + name + '_software`',  # 8
                'DROP TABLE `' + name + '_linux_logon`',  # 9
                'DROP TABLE `' + name + '_users`',  # 10
                'DROP TABLE `' + name + '_virus`',  # 11
                'DROP TABLE `' + name + '_win_logon`'  # 12
            ]

        elif evidenceType == '2':
            sql = [
                'DROP TABLE `' + name + '_files`',  # 1
                'DROP TABLE `' + name + '_virus`'  # 2
            ]

        for i in range(len(sql)):
            print str(i)
            cursor.execute(sql[i])

        db.commit()
        result = True
    except:
        print ' [Error]: Tables couldn\'t be deleted.\n'

    return result

# END EVIDENCE DATABASE


if __name__ == '__main__':
    print '[ERROR]: setup.py can only be opened by pythronic.py.'
