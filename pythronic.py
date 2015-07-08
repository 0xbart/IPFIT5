"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz
"""
from virus_total_apis import PublicApi as VirusTotalPublicApi
from sys import platform as _platform
from time import gmtime, strftime
from psutil import virtual_memory
from datetime import datetime
from subprocess import call
import os
import re
import sys
import time
import glob
import math
import json
import setup
import signal
import socket
import psutil
import shutil
import hashlib
import getpass
import os.path
import sqlite3
import platform
import pyperclip
import functions
import pyautogui
import subprocess
import webbrowser

try:
    from _winreg import *
    import wmi
except:
    pass


opeSys = None
opeSysSlash = None
user = None
userID = None
casenr = None
casename = None

VTotalAPI = 'c5fe9c9e314948e0ede7a412bb2265a54596a4a3c61abf03e7af07c4f12237b5'


def __init__():
    #  Refactor
    pass


def main():
    detectOs()
    startApplication()
    login()
    getCase()
    menu()


def startApplication():
    if not os.path.isfile('db' + functions.getOsSlash() + 'pythronic.db'):
        printWelcomeScreen()
        print (' [INFO]: Database doesn\'t exist; executing setup.\n')
        setup.createDatabase()

    functions.appendLog('i', 'Application Pythronic started.')

    datapath = 'data'
    path = os.path.realpath(datapath)
    printWelcomeScreen()

    try:
        if not os.path.exists(datapath):
            os.mkdir(path)
    except:
        print ' [ERROR]: Data dir does not exist!'
        pass

    databasepath = 'db'
    path = os.path.realpath(databasepath)
    printWelcomeScreen()

    try:
        if not os.path.exists(databasepath):
            os.mkdir(path)
    except:
        print ' [ERROR]: DB dir does not exist!'
        pass

    casespath = 'db' + opeSysSlash + 'cases'
    path = os.path.realpath(casespath)
    printWelcomeScreen()

    try:
        if not os.path.exists(casespath):
            os.mkdir(path)
    except:
        print ' [ERROR]: Cases dir does not exist!'
        pass


def detectOs():
    global opeSys
    global opeSysSlash

    if _platform == 'linux' or _platform == 'linux2':
        opeSys = 'linux'
        opeSysSlash = '/'
    elif _platform == 'darwin':
        opeSys = 'osx'
        opeSysSlash = '/'
    elif _platform == 'win32':
        opeSys = 'windows'
        opeSysSlash = '\\'

    return None


def printWelcomeScreen():
    clearScreen()

    print('''
    ----------------------
    WELCOME TO PYTHRONIC
    ----------------------
             \   ^__^'
              \  (oo)\_______
                 (__)\       )\/\\
                     ||----w |
                     ||     ||''')

    print ''

    message = ''

    if user:
        message += ' Welcome ' + str(user) + '.\n'

    if casenr:
        message += ' Casenumber: ' + str(casenr) + '.\n'
        message += ' Casename: ' + str(casename) + '.\n'

    message += '\n #################################\n\n'

    print message


def clearScreen():
    global opeSys

    if opeSys == 'linux' or opeSys == 'osx':
        os.system('clear')
    elif opeSys == 'windows':
        os.system('cls')


def login():
    print ' Login first:\n'

    global user
    global userID
    user = None
    userID = None

    while True:
        username = functions.askInput('Enter username', 's')
        password = functions.askInput('Enter password', 's')

        if functions.checkLogin(username, password):
            user = username
            userID = functions.getUserID(username)
            break
        else:
            print '\n Login failed, try again. \n'

    return user


def waitUserKeyInput():
    functions.askInput('\n Press enter to continue...', 's')
    return True


def newCase():
    result = False
    printWelcomeScreen()
    while True:
        print ' Creating new case\n'
        name = functions.askInput('Enter name case', 's')
        desc = functions.askInput('Enter description case', 's')
        if name.isalpha():
            if functions.createCase(name, desc, user):
                #  Create own data dir
                datapath = 'data' + opeSysSlash + name
                path = os.path.realpath(datapath)

                try:
                    if not os.path.exists(datapath):
                        os.mkdir(path)
                except:
                    pass

                print ' [INFO]: Case succesfully created.'
                result = functions.getCaseID(name)
                break
        else:
            print '\n [ERROR]: Name must be an alphabetic string, no spaces.\n'
    return result


def getCase():
    printWelcomeScreen()
    while True:
        print ' 1. New case\n 2. Load case\n 3. Delete case\n 4. Manage users'
        print '\n 8. Mousejiggler\n 9. Virus checker'
        print '\n h. Open FAQ\n b. Log out\n q. Quit Pythronic\n\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 'b':
            clearUserDetails()
            clearScreen()
            print ' \n Succesfully logged out.\n\n'
            login()
            printWelcomeScreen()
        elif choice == 1:
            new = newCase()
            if new:
                details = getCaseDetails(new)
                if details:
                    break
            else:
                print '\n  [ERROR]: while creating new case.'
        elif choice == 2 or choice == 3:
            cases = functions.getCases()
            if len(cases) > 0:
                if choice == 2:
                    case = manageCase(cases, 'select')
                    if case:
                        break
                elif choice == 3:
                    case = manageCase(cases, 'delete')
                    if case:
                        print ' [INFO]: Case (nr ' + case + ') deleted!'
            else:
                print '\n No cases found in the database.\n'
        elif choice == 4:
            manageUsers()
        elif choice == 8:
            printWelcomeScreen()
            print ' [INFO]: Mouse jiggler starting. Press CTRL-C to abort.\n'
            try:
                count = 0
                pxl = 10
                while True:
                    x, y = pyautogui.position()
                    if count % 2 == 1:
                        pyautogui.moveTo(int(x)+int(pxl), None)
                    else:
                        pyautogui.moveTo(int(x)-int(pxl), None)
                    count = count + 1
            except:
                pass
            printWelcomeScreen()
            print ' [INFO]: Stopping mouse jiggler.\n'
        elif choice == 9:
            try:
                printWelcomeScreen()
                scanPath = None

                while True:
                    print ' Enther the full path to scan. Type `exit` to exit.'
                    DIR = functions.askInput('Enter path', 's')
                    if not os.path.exists(DIR):
                        print('\n [ERROR]: Dir does not exist!\n')
                    if DIR.lower() == 'exit':
                        break
                    else:
                        scanPath = DIR
                        printWelcomeScreen()
                        break

                logPath = (os.getcwd() + opeSysSlash + 'data' + opeSysSlash +
                           'VIRUSSCAN_' + time.strftime('%Y-%m-%d_%H-%M-%S') +
                           '.log')
                stepCount = 0
                hashList = []
                fullList = []
                hashtag = ' #'
                printWelcomeScreen()
                print ' [INFO]: Malware scan starting;  CTRL-C to abort.\n'
                print ' Calculate file hash, pleas wait...\n'

                for root, dirs, files in os.walk(scanPath):
                    if len(hashtag) < 100:
                        sys.stdout.write("\r" + hashtag)
                        sys.stdout.flush()
                    for fpath in [os.path.join(root, f) for f in files]:
                        name = os.path.relpath(fpath, scanPath)
                        md5 = functions.filehash(fpath)
                        hashList.append(md5)
                        fullList.append(md5)
                        fullList.append(name)
                    hashtag += '#'

                print '\n\n [INFO]: File hash succesfully, scan started.\n'

                for i, item in enumerate(hashList):
                    stepCount = stepCount + 1
                    vt = VirusTotalPublicApi(VTotalAPI)
                    response = vt.get_file_report(item)
                    with open(logPath, 'w') as textfile:
                        textfile.write(json.dumps(response,
                                                  textfile,
                                                  sort_keys=False,
                                                  indent=4))
                    display = manageVirusInfoMessage(stepCount, hashList)
                    sys.stdout.write("\r" + display)
                    sys.stdout.flush()
                    time.sleep(15)

                b = open(logPath)
                positiveCounter = 0
                for line in b:
                    if re.match("(.*)(positives)(.*)[1-99]", line):
                        positiveCounter = positiveCounter + 1
                if positiveCounter >= 1:
                    count = str(positiveCounter)
                    print '\n There are ' + count + ' file(s) infected.'
                else:
                    print '\n You are free of any known malicious software'

                print '\n [INFO]: Scan completed succesfully!'
                print '\n Logfile path: ' + logPath
                waitUserKeyInput()
                printWelcomeScreen()
            except:
                printWelcomeScreen()
                print ' [INFO]: Scan malware checker aborted!\n'
        else:
            print '\n Wrong input, try again!\n'


def manageUsers():
    printWelcomeScreen()
    while True:
        print ' 1. New user\n 2. Delete user\n\n b. Back to menu\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 'b':
            printWelcomeScreen()
            break
        elif choice == 1 or choice == 2:
            if choice == 1:
                if manageUser('new'):
                    printWelcomeScreen()
                    print (' [INFO]: User succesfully added to the '
                           'database.\n')
            if choice == 2:
                if manageUser('delete'):
                    printWelcomeScreen()
                    print ' User succesfully deleted.\n'
        else:
            print '\n Wrong input, try again!\n'


def manageUser(action):
    result = False
    printWelcomeScreen()
    if action == 'new':
        while True:
            print ' Create new user, follow instructions:\n'
            while True:
                username = functions.askInput('Enter username', 's')
                if len(username) >= 4:
                    if not functions.checkUserExist(username):
                        break
                    else:
                        print '\n [ERROR]: Username exist, try another name.\n'
                else:
                    print ' [ERROR]: Username must be longer then 3 char.\n'
            password = functions.askInput('Enter password', 's')
            if len(username) >= 4:
                if functions.createUser(username, password):
                    result = True
                    break
                else:
                    print '\n [ERROR]: User cannot be created!\n'
                    break
            else:
                print ' [ERROR]: Choose a password longer then 3 char.\n'

    elif action == 'delete':
        users = functions.getUsers()
        if len(users) > 1:
            userIDs = functions.getUserIDs()
            print ' Delete user, follow instructions:\n'
            while True:
                for user in users:
                    if not str(user[0]) == str(userID):
                        print(' {0}: {1}'.format(user[0], user[1]))
                print '\n b. Back to menu.'
                choice = functions.askInput('\n Make a choice', 'i')
                if choice == 'q' or choice == 'h':
                    globalOperators(choice)
                elif choice == 'b':
                    getCase()
                elif choice in userIDs:
                    if not str(choice) == str(userID):
                        username = functions.getUsername(str(choice))
                        question = '[WARNING]: Deleting `' + username + '`? '
                        question += 'Y = yes, P = permanently, other = abort'
                        confirm = functions.askInput(question, 's')
                        if confirm.lower() == 'y' or confirm.lower() == 'p':
                            functions.deleteUser(str(choice), confirm.lower())
                            result = True
                        printWelcomeScreen()
                        break
                    else:
                        print '\n You cannot delete yourself!\n'
                else:
                    print '\n Wrong input, try again!\n'
        else:
            print ' [ERROR]: No other users found.\n'
    return result


def manageVirusInfoMessage(stepCount, hashList):
    timeToGo = (int(len(hashList)) - stepCount) * 15 / 60
    itemsLeft = (int(len(hashList)) - stepCount)
    string = (' There are ' + str(itemsLeft) + ' item(s) left to be '
              'verified. Time for completion: ' + str(timeToGo) +
              ' minutes.')
    return string


def manageCase(cases, action):
    printWelcomeScreen()
    casesNumbers = functions.getCasesNumbers()
    casenr = None

    print ' Following cases are found:\n'

    while True:
        for case in cases:
            print(' {0}: {1}'.format(case[0], case[1]))
        print '\n b. Back to menu.'
        choice = functions.askInput('\n Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 'b':
            getCase()
        elif choice in casesNumbers:
            details = getCaseDetails(choice)
            if action == 'select':
                if details:
                    casenr = choice
                    break
            elif action == 'delete':
                question = '[WARNING]: Deleting `' + casename + '`? '
                question += 'Y = yes, P = permanently, other = abort'
                confirm = functions.askInput(question, 's')
                if confirm.lower() == 'y' or confirm.lower() == 'p':
                    functions.deleteCase(str(choice), confirm.lower())

                    if confirm.lower() == 'p':
                        #  Clear case data path
                        datapath = 'data' + opeSysSlash + casename
                        path = os.path.realpath(datapath)
                        try:
                            if os.path.exists(datapath):
                                shutil.rmtree(path, ignore_errors=True)
                        except:
                            pass

                clearCaseDetails()
                printWelcomeScreen()
                break
        else:
            print '\n Wrong input, try again!\n'

    return casenr


def getCaseDetails(ID):
    result = False

    try:
        global casenr
        global casename
        casenr = ID
        casename = functions.getCaseName(str(ID))
        result = True
    except:
        print ' [ERROR]: Cannot get case details.'

    return result


def clearCaseDetails():
    global casenr
    global casename
    casenr = None
    caseName = None

    return True


def clearUserDetails():
    global user
    global userID
    user = None
    userID = None

    return True


def menu():
    printWelcomeScreen()
    while True:
        evidences = functions.getEvidences(casename)
        evidenceIDs = functions.getEvidenceIDs(casename)
        print ' 1. New evidence\n 2. Delete evidence\n 3. Start scan'
        print ' 4. Generate report\n'
        print ' h. Open FAQ\n b. Exit case\n q. Quit Pythronic\n\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 'b':
            clearCaseDetails()
            getCase()
            menu()
        elif choice == 1:
            new = newEvidence()
            if new:
                printWelcomeScreen()
                print ' [INFO]: Evidence ' + new + ' created succesfully!\n'
            else:
                printWelcomeScreen()
                print ' [ERROR]: while creating new evidence.\n'
        elif choice == 2:
            if len(evidences) > 0:
                printWelcomeScreen()
                print ' Delete evidence, follow instructions:\n'
                while True:
                    for evidence in evidences:
                        print(' {0}: {1}'.format(evidence[0], evidence[1]))
                    print '\n b. Back to menu.'
                    choice = functions.askInput('\n Make a choice', 'i')
                    if choice == 'q' or choice == 'h':
                        globalOperators(choice)
                    elif choice == 'b':
                        printWelcomeScreen()
                        break
                    elif choice in evidenceIDs:
                        evidence = functions.getEvidence(casename, str(choice))
                        question = '[WARNING]: Deleting `' + evidence + '`? '
                        question += 'Y = yes, P = permanently, other = abort'
                        confirm = functions.askInput(question, 's')
                        if confirm.lower() == 'y' or confirm.lower() == 'p':
                            name = str(casename)
                            ID = str(choice)
                            oper = str(confirm.lower())
                            if functions.deleteEvidence(name, ID, oper):
                                printWelcomeScreen()
                                print (' [INFO]: Evidence ' + evidence +
                                       ' deleted succesfully!\n')
                                break
                            else:
                                printWelcomeScreen()
                                print (' [ERROR]: Evidence ' + evidence +
                                       ' cannot be deleted!\n')
                                break
                        else:
                            printWelcomeScreen()
                            break
                    else:
                        printWelcomeScreen()
                        print ' Wrong input, try again!\n'
            else:
                printWelcomeScreen()
                print ' [ERROR]: No evidences found.\n'
        elif choice == 3:
            if len(evidences) > 0:
                printWelcomeScreen()
                print ' Start scan, follow instructions:'
                while True:
                    print ' Select evidence to start scan.\n'
                    for evidence in evidences:
                        print(' {0}: {1}'.format(evidence[0], evidence[1]))
                    print '\n b. Back to menu.'
                    choice = functions.askInput('\n Make a choice', 'i')
                    if choice == 'q' or choice == 'h':
                        globalOperators(choice)
                    elif choice == 'b':
                        printWelcomeScreen()
                        break
                    elif choice in evidenceIDs:
                        eID = str(choice)
                        eName = functions.getEvidence(casename, str(choice))
                        dtime = time.strftime("%Y-%m-%d %H:%M:%S")
                        overview = ('\n Scan will start now on (' + dtime + ')'
                                    ' on (case: ' + casename + ', evidence: ' +
                                    eName + ') by user ' + user + '.')
                        confirm = ('Are you authorized to do this? '
                                   'Press Y to proceed')
                        choiceScan = functions.askInput(confirm, 's')
                        if choiceScan.lower() == 'y':
                            eType = functions.getEvidenceType(casename, eID)
                            if startScan(casename, eName, eType):
                                printWelcomeScreen()
                                print (' [INFO]: Scan on ' + eName +
                                       ' succesfully completed!\n')
                                break
                            else:
                                printWelcomeScreen()
                                print (' [INFO]: Scan on ' + eName +
                                       ' failed!\n')
                                break
                        else:
                            printWelcomeScreen()
                            print ' [INFO]: Scan aborted.\n'
                            break
            else:
                printWelcomeScreen()
                print ' [ERROR]: No evidences found, add first an evidence.\n'
        elif choice == 4:
            print 'rapport bouwen'
        else:
            print '\n Wrong input, try again!\n'


def newEvidence():
    result = False
    evidenceTypes = ['1', '2']
    sEtype = ('\n Type evidence: \n\n 1: Computer / Laptop / Server\n '
              '2: Device (USB, SD, HDD)\n\n Enter type evidence ID')
    printWelcomeScreen()
    while True:
        print ' Creating new evidence\n'
        name = functions.askInput('Enter name evidence', 's')
        desc = functions.askInput('Enter description evidence', 's')
        etype = functions.askInput(sEtype, 's')
        if name.isalpha() and etype in evidenceTypes:
            if functions.createEvidence(name, desc, casename, etype):
                result = name
                break
        else:
            if etype not in evidenceTypes:
                printWelcomeScreen()
                print ' [ERROR]: EvidenceType is not a valid choice.\n'
            else:
                printWelcomeScreen()
                print (' [ERROR]: Name must be an alphabetic '
                       'string, no spaces.\n')
    return result


def globalOperators(choice):
    if choice == 'h':
        print ' [INFO]: FAQ opened in browser.'
        FAQfile = 'FAQ' + functions.getOsSlash() + 'index.html'
        webbrowser.open('file://' + os.path.realpath(FAQfile))
    elif choice == 'q':
        sys.exit(0)


def signal_handler(signal, frame):
    sys.exit(0)


def getCaseDatabase(casename):
    detectOs()
    dbpath = ('db' + opeSysSlash + 'cases' + opeSysSlash + casename + '.db')
    path = os.path.realpath(dbpath)
    return path


#  SCAN ITEMS


def startScan(casename, eName, eType):
    result = False

    if eType == '1':
        ROOT = None

        #  PC / Laptop scan
        printWelcomeScreen()
        print ' Want to index a (specific) path?\n'
        confirm = 'Press Y for path input'
        askFilesPathScan = functions.askInput(confirm, 's')
        if askFilesPathScan.lower() == 'y':
            while True:
                askPath = '\n Enter path'
                pathInput = functions.askInput(askPath, 's')
                if os.path.isdir(pathInput):
                    ROOT = pathInput
                    break
                else:
                    print '\n No valid input, try again!\n'

        print '\n [INFO]: Scan on evidence ' + eName + ' started.\n'

        if scanComputerGeneral(casename, eName):
            print ' [X]', 'General settings completed.'
        else:
            print ' [ ]', 'General settings passed.'

        if scanComputerHardware(casename, eName):
            print ' [X]', 'Hardware settings completed.'
        else:
            print ' [ ]', 'Hardware settings passed.'

        if scanComputerStartup(casename, eName):
            print ' [X]', 'Startup settings completed.'
        else:
            print ' [ ]', 'Startup settings passed.'

        if scanComputerCloud(casename, eName):
            print ' [X]', 'Cloud settings completed.'
        else:
            print ' [ ]', 'Cloud settings passed.'

        if scanComputerHistory(casename, eName):
            print ' [X]', 'History settings completed.'

        if scanComputerSoftware(casename, eName):
            print ' [X]', 'Software settings completed.'
        else:
            print ' [ ]', 'Software settings passed.'

        if scanComputerDrives(casename, eName):
            print ' [X]', 'Drives settings completed.'
        else:
            print ' [ ]', 'Software settings passed.'

        if scanComputerPslist(casename, eName):
            print ' [X]', 'Process settings completed.'
        else:
            print ' [ ]', 'Software settings passed.'

        if scanComputerNetwork(casename, eName):
            print ' [X]', 'Network settings completed.'
        else:
            print ' [ ]', 'Software settings passed.'

        if ROOT:
            if scanEvidenceHash(casename, eName, ROOT):
                print ' [X]', 'Dir file hash completed.'
            else:
                print ' [ ]', 'Dir file hash passed.'

            if scanEvidenceFileHierarchie(casename, eName, ROOT):
                print ' [X]', 'Dir file hierarchie completed.'
            else:
                print ' [ ]', 'Dir file hierarchie passed.'

        print '\n [INFO]: Scan successfully ended!'
        waitUserKeyInput()
        result = True
    elif eType == '2':
        ROOT = None

        #  Device scan
        printWelcomeScreen()
        print ' Enter the devide path (case sensitive).\n'
        while True:
            askPath = '\n Enter path'
            pathInput = functions.askInput(askPath, 's')
            if os.path.isdir(pathInput):
                ROOT = pathInput
                break
            else:
                print '\n No valid input, try again!\n'

        if ROOT:
            if scanEvidenceHash(casename, eName, ROOT):
                print ' [X]', 'Dir file hash completed.'
            else:
                print ' [ ]', 'Dir file hash passed.'

            if scanEvidenceFileHierarchie(casename, eName, ROOT):
                print ' [X]', 'Dir file hierarchie completed.'
            else:
                print ' [ ]', 'Dir file hierarchie passed.'

        print '\n [INFO]: Scan successfully ended!'
        waitUserKeyInput()
        result = True

    return result


def scanComputerGeneral(casename, eName):
    result = False

    try:
        ddate = time.strftime("%Y-%m-%d")
        ttime = time.strftime("%H:%M:%S")
        timezone = strftime("%z", gmtime())
        clipboard = pyperclip.paste()
        computername = socket.gethostname()
        username = getpass.getuser()
        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()
        cursor.execute('INSERT INTO `' + eName + '_general`'
                       '(os, ddate, ttime, timezone, clip_out, pc_name, '
                       'username) VALUES (?,?,?,?,?,?,?)',
                       (opeSys, ddate, ttime, timezone, clipboard,
                        computername, username))
        db.commit()

        result = True
    except:
        pass

    return result


def scanComputerHardware(casename, eName):
    result = False

    try:
        if opeSys == 'linux' or opeSys == 'linux2':
            processor = os.popen("grep 'model name' /proc/cpuinfo")
            system_arch = platform.architecture()
            total_memory = os.popen("cat /proc/meminfo | grep "
                                    "MemTotal | awk '{ print $2 }'").read()

            db = sqlite3.connect(getCaseDatabase(casename))
            cursor = db.cursor()
            cursor.execute('INSERT INTO `' + eName + '_hardware` ('
                           'processor, system_arch, total_memory) '
                           'VALUES (?,?,?)',
                           (str(processor), str(system_arch),
                            str(total_memory)))
            db.commit()

            result = True
        elif opeSys == 'darwin' or opeSys == 'osx':
            processor = platform.processor()
            system_arch = platform.version()
            proc_name = platform.node()
            proc_family = platform.machine()

            db = sqlite3.connect(getCaseDatabase(casename))
            cursor = db.cursor()
            cursor.execute('INSERT INTO `' + eName + '_hardware` ('
                           'processor, system_arch, proc_name, proc_family) '
                           'VALUES (?,?,?,?)',
                           (processor, system_arch, proc_name, proc_family))
            db.commit()

            result = True
        elif opeSys == 'win32' or opeSys == 'windows':
            mem = virtual_memory()
            c = wmi.WMI()
            for i in c.Win32_Processor():
                cputype = i.Name

            processor = cputype
            system_arch = platform.machine()
            proc_family = platform.processor()
            used_memory = str((mem.used/(math.pow(2, 30))))
            free_memory = str((mem.available/(math.pow(2, 30))))
            total_memory = str((mem.total/(math.pow(2, 30))))

            db = sqlite3.connect(getCaseDatabase(casename))
            cursor = db.cursor()
            cursor.execute('INSERT INTO `' + eName + '_hardware` ('
                           'processor, system_arch, proc_family, used_memory, '
                           'free_memory, total_memory) VALUES (?,?,?,?,?,?)',
                           (processor, system_arch, proc_family, used_memory,
                            free_memory, total_memory))
            db.commit()

            result = True
    except:
        pass

    return result


def scanComputerStartup(casename, eName):
    result = False

    try:
        if opeSys == 'linux' or opeSys == 'linux2':
            items = subprocess.call(['initctl show-config'], shell=True)
            db = sqlite3.connect(getCaseDatabase(casename))
            cursor = db.cursor()
            cursor.execute('INSERT INTO `' + eName + '_linux_logon` ('
                           'name) VALUES (?)', (items))
            db.commit()
            result = True
        elif opeSys == 'win32' or opeSys == 'windows':
            startUpItems = []
            aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")

            for i in range(1024):
                try:
                    n, v, t = EnumValue(aKey, i)
                    startUpItems.append(n)
                except:
                    pass

            db = sqlite3.connect(getCaseDatabase(casename))
            cursor = db.cursor()

            for i in range(len(startUpItems)):
                cursor.execute('INSERT INTO `' + eName + '_win_logon` ('
                               'name) VALUES (?)', (str(startUpItems[i]),))

            db.commit()

            result = True
    except:
        pass

    return result


def scanComputerCloud(casename, eName):
    result = False

    try:
        googledrive = 0
        dropbox = 0
        onedrive = 0
        evernote = 0

        if _platform == 'win32':
            if os.path.isdir("C:\\Program Files (x86)\\Google\\Drive"):
                googledrive = 1
            for p in psutil.process_iter():
                try:
                    if p.name() == 'googledrivesync.exe':
                        googledrive = 1
                except psutil.Error:
                    pass

            if os.path.isdir("C:\\Program Files (x86)\\dropbox"):
                dropbox = 1
            else:
                for p in psutil.process_iter():
                    try:
                        if p.name() == 'dropbox.exe':
                            dropbox = 1
                            dropbox.append(p)
                    except psutil.Error:
                        pass

            if os.path.isdir("C:\\Program Files (x86)\\Microsoft onedrive"):
                onedrive = 1
                for p in psutil.process_iter():
                    try:
                        if p.name() == 'onedrive.exe':
                            onedrive = 1
                            one_drive.append(p)
                    except psutil.Error:
                        pass

            if os.path.isdir("C:\\Program Files (x86)\\evernote"):
                evernote = 1
                for p in psutil.process_iter():
                    try:
                        if p.name() == 'evernote.exe':
                            evernote = 1
                            evernote.append(p)
                    except psutil.Error:
                        pass

        if _platform == 'linux' or _platform == "darwin":
            for p in psutil.process_iter():
                try:
                    if p.name() == 'Google Drive':
                        googledrive = 1
                except psutil.Error:
                    pass

            for p in psutil.process_iter():
                try:
                    if p.name() == 'Dropbox':
                        dropbox = 1
                except psutil.Error:
                    pass

            for p in psutil.process_iter():
                try:
                    if p.name() == 'OneDrive':
                        onedrive = 1
                except psutil.Error:
                    pass

            for p in psutil.process_iter():
                try:
                    if p.name() == 'Evernote':
                        evernote = 1
                except psutil.Error:
                    pass

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()
        cursor.execute('INSERT INTO `' + eName + '_cloud` (googledrive, '
                       'dropbox, onedrive, evernote) VALUES (?,?,?,?)',
                       (googledrive, dropbox, onedrive, evernote))
        db.commit()
        result = True
    except:
        pass

    return result


def scanComputerHistoryChromeWin(name, dest):
    result = False

    try:
        path = ("C:\\Users\%s\AppData\Local\Google\Chrome"
                "\User Data\Default\History")
        chrome = (path % name)
        shutil.copy2(chrome, dest)
        destSl = dest + opeSysSlash
        os.rename(destSl + 'History', destSl + 'Chrome_History')
        result = True
    except:
        pass

    return result


def scanComputerHistoryChromeLinux(name, dest):
    result = False

    try:
        chrome = ("/home/%s/.config/google-chrome/Default/History" % name)
        shutil.copy2(chrome, dest)
        destSl = dest + opeSysSlash
        os.rename(destSl + 'History', destSl + 'Chrome_History')
        result = True
    except:
        pass

    return result


def scanComputerHistoryChromeOsx(name, dest):
    result = False

    try:
        chromePath = ("/Users/%s/Library/Application Support/"
                      "Google/Chrome/Default//History")
        chrome = (chromePath % name)
        shutil.copy2(chrome, dest)
        destSl = dest + opeSysSlash
        os.rename(destSl + 'History', destSl + 'Chrome_History')
        result = True
    except:
        pass

    return result


def scanComputerHistoryIe(name, dest):
    result = False

    try:
        pathOne = ("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer"
                   "\IECompatData\\")
        pathTwo = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\")
        pathThree = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\")
        if os.path.isfile(pathOne % name):
            internet = (pathOne % name)
            shutil.copy2(internet, dest)
            result = True
        if os.path.isfile(pathTwo % name):
            internet = (pathTwo % name)
            shutil.copy2(internet, dest)
            result = True
        if os.path.isfile(pathThree % name):
            internet = (pathThree % name)
            shutil.copy2(internet, dest)
            result = True
    except:
        pass

    return result


def scanComputerHistoryFirefoxWin(name, dest):
    result = False

    try:
        basePath = ("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\\Profiles")
        osfirefox = os.listdir(basePath % name)
        osfirefoxformat = (str(osfirefox)[2:-2])
        firefoxPath = ("C:\\Users\%s\AppData\Roaming\Mozilla\""
                       "Firefox\Profiles\%s\\places.sqlite")
        firefox = (firefoxPath % (name, osfirefoxformat))
        shutil.copy2(firefox, dest)
        destSl = dest + opeSysSlash
        os.rename(destSl + 'places.sqlite', destSl + 'firefox_places.sqlite')
        result = True
    except:
        pass

    return result


def scanComputerHistoryFirefoxLinux(name, dest):
    result = False
    current = os.getcwd()

    try:
        os.chdir("/home/%s/.mozilla/firefox" % name)
        for file in glob.glob("*.default"):
            firefoxPath = "/home/%s/.mozilla/firefox/%s/places.sqlite"
            firefox = (firefoxPath % (name, file))
            shutil.copy2(firefox, dest)
            destSl = dest + opeSysSlash
            os.rename(destSl + 'places.sqlite', destSl + 'frfox_places.sqlite')
            result = True
    except:
        pass
    finally:
        os.chdir(current)

    return result


def scanComputerHistoryFirefoxOsx(name, dest):
    result = False
    current = os.getcwd()

    try:
        n = name
        os.chdir("/Users/%s/Library/Application Support/Firefox/Profiles" % n)
        for file in glob.glob("*.default"):
            firefoxPath = ("/Users/%s/Library/Application Support/Firefox/"
                           "Profiles/%s/places.sqlite")
            firefox = (firefoxPath % (name, file))
            shutil.copy2(firefox, dest)
            destSl = dest + opeSysSlash
            os.rename(destSl + 'places.sqlite', destSl + 'frfox_places.sqlite')
            result = True
    except:
        pass
    finally:
        os.chdir(current)

    return result


def scanComputerHistory(casename, eName):
    result = False

    try:
        username = getpass.getuser()

        his_iexplorer = 0
        his_ff = 0
        his_chrome = 0

        datapath = 'data' + opeSysSlash + casename + opeSysSlash + eName
        path = os.path.realpath(datapath)

        try:
            if not os.path.exists(datapath):
                os.mkdir(path)
        except:
            pass

        if _platform == 'win32':
            if scanComputerHistoryIe(username, path):
                his_iexplorer = 1
            if scanComputerHistoryChromeWin(username, path):
                his_chrome = 1
            if scanComputerHistoryFirefoxWin(username, path):
                his_ff = 1
        elif _platform == "linux" or _platform == "linux2":
            if scanComputerHistoryChromeLinux(username, path):
                his_chrome = 1
            if scanComputerHistoryFirefoxLinux(username, path):
                his_ff = 1

        elif _platform == "darwin":
            if scanComputerHistoryChromeOsx(username, path):
                his_chrome = 1
            if scanComputerHistoryFirefoxOsx(username, path):
                his_ff = 1

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()
        cursor.execute('INSERT INTO `' + eName + '_browser`'
                       '(his_chrome, his_ff, his_iexplorer)'
                       'VALUES (?,?,?)', (his_chrome, his_ff, his_iexplorer))
        db.commit()
        result = True
    except:
        pass

    return result


def scanComputerSoftware(casename, eName):
    result = False

    softwarelist = []

    try:
        if _platform == 'win32':
            uninstall = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            regcontent = OpenKey(uninstall, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            for i in range(1024):
                try:
                    keyname = EnumKey(regcontent, i)
                    regdata = OpenKey(regcontent, keyname)
                    entries = QueryValueEx(regdata, "DisplayName")
                    softwarelist.append(entries)
                except WindowsError:
                    pass

            uninstall = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            regcontent = OpenKey(uninstall, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
            for i in range(1024):
                try:
                    keyname = EnumKey(regcontent, i)
                    asubkey = OpenKey(regcontent, keyname)
                    entries = QueryValueEx(asubkey, "DisplayName")
                    softwarelist.append(entries)
                except WindowsError:
                    pass
            uniquelist = list(set(softwarelist))
            uniquelist.sort()

            db = sqlite3.connect(getCaseDatabase(casename))
            cursor = db.cursor()

            for software in uniquelist:
                try:
                    cursor.execute('INSERT INTO `' + eName + '_software` ('
                                   'name) VALUES (?)', (software[0],))
                except:
                    pass

            db.commit()
            result = True
    except:
        pass

    return result


def scanComputerDrives(casename, eName):
    result = False

    try:
        disklist = []
        diskinfo = str(psutil.disk_partitions())
        for match in re.findall('[A-Z]{1}[:]{1}|[/][d][e][v][/][a-z]{3,4}[0-9]'
                                '{0,2}[a-z]{0,2}[0-9]|[/][\']|[/][V][a-z]'
                                '{0,12}[/][A-Z]{0,12}|[N][T][F][S]|[n][t]'
                                '[f][s]|[e][x][t][2-4]|[e]{0,1}[x]{0,1}[F][A]'
                                '[T]|[h][f][s]|[R][e][F][S]', diskinfo):
            disklist.append(match)

        countDisks = len(disklist) / 3
        count = 0

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()

        for disk in range(countDisks):
            cursor.execute('INSERT INTO `' + eName + '_drive`'
                           '(drive_name, drive_mountpoint, drive_filesystem'
                           ') VALUES (?,?,?)',
                           (disklist[count],
                            disklist[(count + 1)],
                            disklist[(count + 2)]))
            count = count + 3

        db.commit()

        result = True
    except:
        pass

    return result


def scanComputerPslist(casename, eName):
    result = False

    try:
        processes = []

        for proc in psutil.process_iter():
            processes.append(proc.name)

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()

        for process in processes:
            cursor.execute('INSERT INTO `' + eName + '_pslist`'
                           '(name) VALUES (?)', (str(process),))

        db.commit()

        result = True
    except:
        pass

    return result


def scanComputerNetwork(casename, eName):
    result = False
    opeSysSlash = '/'

    try:
        datapath = 'data' + opeSysSlash + casename + opeSysSlash + eName
        path = os.path.realpath(datapath)

        try:
            if not os.path.exists(datapath):
                os.mkdir(path)
        except:
            pass

        logPath = path + opeSysSlash + 'networking.txt'

        if _platform == 'win32':
            with open(logPath, 'w') as outfile:
                subprocess.call('ipconfig.exe /all', stdout=outfile)
        elif _platform == 'darwin' or _platform == 'linux':
            with open(logPath, 'w') as outfile:
                subprocess.call("ifconfig", stdout=outfile)

        unixKeywords = ['inet']
        windowsKeywords = ['IP', 'DHCP']
        temp = []

        if _platform == 'win32':
            with open(logPath, 'r') as file_to_read:
                for line in file_to_read:
                    for i, j in enumerate(windowsKeywords):
                        if j in line:
                            temp.append(line + ',')
        elif _platform == 'darwin' or _platform == 'linux':
            with open(logPath, 'r') as file_to_read:
                for line in file_to_read:
                    for i, j in enumerate(unixKeywords):
                        if j in line:
                            temp.append(line)

        iplist = []
        for i, line in enumerate(open(logPath)):
            for match in re.findall(r'[0-9]+(?:\.[0-9]+){3}', line):
                iplist.append(match)

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()
        for i in range(len(iplist)):
            cursor.execute('INSERT INTO `' + eName + '_network`'
                           '(ip) VALUES (?)', (str(iplist[i]),))

        db.commit()
        result = True
    except:
        pass

    return result


def scanEvidenceHash(casename, eName, ROOT):
    result = True

    try:
        countFiles = 0
        allFiles = []

        for root, dirs, files in os.walk(ROOT):
            for fpath in [os.path.join(root, f) for f in files]:
                size = os.path.getsize(fpath)
                sha = functions.filehash(fpath)
                name = os.path.relpath(fpath, ROOT)

                allFiles.append([])
                allFiles[countFiles].append(('size', size))
                allFiles[countFiles].append(('sha', sha))
                allFiles[countFiles].append(('name', name))

                countFiles = countFiles + 1

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()
        for i in range(len(allFiles)):
            cursor.execute('INSERT INTO `' + eName + '_files` ('
                           'name, size, shahash) '
                           'VALUES (?,?,?)',
                           (allFiles[i][2][1],
                            allFiles[i][0][1],
                            allFiles[i][1][1]))

        db.commit()
    except:
        pass

    return result


def scanEvidenceFileHierarchie(casename, eName, ROOT):
    result = False

    try:
        html = '<ul id="dhtmlgoodies_tree" class="dhtmlgoodies_tree">'
        html += scanEvidenceFileHierarchieAction(ROOT, True)
        html += ('<a href="#" onclick="expandAll(\'dhtmlgoodies_tree\');'
                 'return false">Expand all</a> ')
        html += ('<a href="#" onclick="collapseAll(\'dhtmlgoodies_tree\');'
                 'return false">Collapse all</a>')

        db = sqlite3.connect(getCaseDatabase(casename))
        cursor = db.cursor()
        cursor.execute('INSERT INTO `' + eName + '_files_overview` ('
                       'html_view) VALUES (?)', (html,))
        db.commit()

        result = True
    except:
        pass

    return result


def scanEvidenceFileHierarchieAction(d, first):
    try:
        if first:
            res = ''
        else:
            res = '<ul>'

        lds = os.listdir(d)

        for l in lds:
            if os.path.isdir(os.path.join(d, l)):
                dirPath = os.path.join(d, l)
                res += '<li><a href="#">' + l + '</a>'
                res += scanEvidenceFileHierarchieAction(dirPath, False)
                if not first:
                    res += scanEvidenceFileHierarchieHTML(d)
                res += '</li>'

        if first:
            res += scanEvidenceFileHierarchieHTML(d)
        res += '</ul>'
        html = res.replace('<ul></ul>', '')

        return html
    except:
        pass


def scanEvidenceFileHierarchieHTML(d):
    html = ''

    extImg = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
    extVideo = ['.avi', '.mp4', '.mkv']
    extWord = ['.doc', '.docx', '.dot', 'dotx']
    extExcel = ['.xls', '.xlsx', '.xlt', '.xltx']
    extPower = ['.ppt', '.pptx', '.pot', '.pps', '.potx', 'ppsx']
    extExe = ['.exe']
    extMail = ['.pst']
    extPdf = ['.pdf']
    extRar = ['.rar']
    extZip = ['.zip']
    extText = ['.txt', '.log']

    try:
        path = os.path.isfile(os.path.join(d, f))
        files = [f for f in os.listdir(d) if path]

        for file in files:
            ext = os.path.splitext(file)[1]
            ext = ext.lower()

            if ext in extImg:
                html += ('<li class="dhtmlgoodies_photo.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extVideo:
                html += ('<li class="dhtmlgoodies_video.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extWord:
                html += ('<li class="dhtmlgoodies_word.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extExcel:
                html += ('<li class="dhtmlgoodies_excel.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extPower:
                html += ('<li class="dhtmlgoodies_power.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extExe:
                html += ('<li class="dhtmlgoodies_exe.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extMail:
                html += ('<li class="dhtmlgoodies_mail.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extPdf:
                html += ('<li class="dhtmlgoodies_pdf.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extRar:
                html += ('<li class="dhtmlgoodies_rar.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extZip:
                html += ('<li class="dhtmlgoodies_zip.gif">'
                         '<a href="#">' + file + '</a></li>')
            elif ext in extText:
                html += ('<li class="dhtmlgoodies_txt.gif">'
                         '<a href="#">' + file + '</a></li>')
            else:
                html += ('<li class="dhtmlgoodies_sheet.gif">'
                         '<a href="#">' + file + '</a></li>')
    except:
        pass

    return html


#  END SCAN ITEMS


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
