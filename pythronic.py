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
    while True:
        getCase()
        menu()
        clearCaseDetails()


def startApplication():
    if not os.path.isfile('db' + functions.getOsSlash() + 'pythronic.db'):
        printWelcomeScreen()
        print ' [INFO]: Database doesn\'t exist; executing setup.\n'
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
            functions.appendLog('i', 'User ' + user + ' logged in.')
            break
        else:
            functions.appendLog('w', 'Login failed with username ' + username)
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

                print ' [INFO]: Case successfully created.'
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
        print '\n h. Open manual\n b. Log out\n q. Quit Pythronic\n\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 'b':
            clearUserDetails()
            clearScreen()
            print ' \n successfully logged out.\n\n'
            functions.appendLog('i', 'User ' + user + 'logged out.')
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
                        functions.appendLog('i', 'Case (ID' + case + ') '
                                            'deleted.')
            else:
                print '\n No cases found in the database.\n'
        elif choice == 4:
            manageUsers()
        elif choice == 8:
            printWelcomeScreen()
            print ' [INFO]: Mousejiggler starting. Press CTRL-C to abort.\n'
            functions.appendLog('i', 'Mousejiggler successfully started.')
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
            functions.appendLog('i', 'Mousejiggler successfully stopped.')
        elif choice == 9:
            try:
                printWelcomeScreen()
                functions.appendLog('i', 'Virusscan check started.')
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

                print '\n\n [INFO]: File hash successfully, scan started.\n'

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

                print '\n [INFO]: Scan completed successfully!'
                print '\n Logfile path: ' + logPath
                functions.appendLog('i', 'Virusscan check stopped.')
                waitUserKeyInput()
                printWelcomeScreen()
            except:
                printWelcomeScreen()
                print ' [INFO]: Scan malware checker aborted!\n'
                functions.appendLog('w', 'Virusscan check aborted.')
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
                    print(' [INFO]: User successfully added to the '
                          'database.\n')
            if choice == 2:
                if manageUser('delete'):
                    printWelcomeScreen()
                    print ' User successfully deleted.\n'
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
                    functions.appendLog('i', 'User ' + username + ' created.')
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
                            functions.appendLog('i', 'User ' + username +
                                                ' deleted.')
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
                message = None
                if confirm.lower() == 'y' or confirm.lower() == 'p':
                    if functions.deleteCase(str(choice), confirm.lower()):
                        message = 'Case ' + casename + ' successfully deleted.'
                        functions.appendLog('i', 'Case ' + casename +
                                            ' deleted.')

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
                if message:
                    print ' [INFO]:' + message + '\n'
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
    message = 'Case ' + casename + ' has been opened by ' + user
    functions.appendCaseLog(casename, 'i', message)
    while True:
        evidences = functions.getEvidences(casename)
        evidenceIDs = functions.getEvidenceIDs(casename)
        print ' 1. New evidence\n 2. Delete evidence\n 3. Start scan'
        print ' 4. Generate report\n'
        print ' h. Open manual\n b. Exit case\n q. Quit Pythronic\n\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 'b':
            break
            # clearCaseDetails()
            # getCase()
            # menu()
        elif choice == 1:
            new = newEvidence()
            if new:
                printWelcomeScreen()
                print ' [INFO]: Evidence ' + new + ' created successfully!\n'
                message = 'Evidence ' + new + ' added to the database.'
                functions.appendCaseLog(casename, 'i', message)
            else:
                printWelcomeScreen()
                print ' [ERROR]: while creating new evidence.\n'
                message = 'Evidence ' + new + ' cannot be created.'
                functions.appendCaseLog(casename, 'w', message)
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
                                print(' [INFO]: Evidence ' + evidence +
                                      ' deleted successfully!\n')
                                message = ('Evidence ' + evidence +
                                           'deleted by ' + user + '.')
                                functions.appendCaseLog(casename, 'i', message)
                                break
                            else:
                                printWelcomeScreen()
                                print(' [ERROR]: Evidence ' + evidence +
                                      ' cannot be deleted!\n')
                                message = ('Evidence ' + evidence +
                                           'cannot be deleted.')
                                functions.appendCaseLog(casename, 'w', message)
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
                            message = ('Scan on evidence ' + eName +
                                       ' started by ' + user + '.')
                            functions.appendCaseLog(casename, 'i', message)
                            eType = functions.getEvidenceType(casename, eID)
                            if startScan(casename, eName, eType):
                                printWelcomeScreen()
                                print(' [INFO]: Scan on ' + eName +
                                      ' successfully completed!\n')
                                message = ('Scan on evidence ' + eName +
                                           ' successfully ended.')
                                functions.appendCaseLog(casename, 'i', message)
                                break
                            else:
                                printWelcomeScreen()
                                print(' [INFO]: Scan on ' + eName +
                                      ' failed!\n')
                                message = ('Scan on evidence ' + eName +
                                           'failed!')
                                functions.appendCaseLog(casename, 'w', message)
                                break
                        else:
                            printWelcomeScreen()
                            print ' [INFO]: Scan aborted.\n'
                            message = ('Scan on evidence ' + eName +
                                       'aborted.')
                            functions.appendCaseLog(casename, 'i', message)
                            break
            else:
                printWelcomeScreen()
                print ' [ERROR]: No evidences found, add first an evidence.\n'
        elif choice == 4:
            printWelcomeScreen()
            print ' Start building report, follow instructions:'
            while True:
                print ' Select evidence to start building.\n'
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
                    message = ('Building rapport of case ' + casename + '.')
                    functions.appendCaseLog(casename, 'i', message)
                    eID = str(choice)
                    eName = functions.getEvidence(casename, str(choice))
                    eType = functions.getEvidenceType(casename, eID)

                    if makeRapport(casename, eName, eType):
                        print ' [INFO] Report created successfully!'
                    else:
                        print ' [ERROR] Creating report failed!'

                    waitUserKeyInput()
                    printWelcomeScreen()
                    break
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
                print(' [ERROR]: Name must be an alphabetic '
                      'string, no spaces.\n')
    return result


def globalOperators(choice):
    if choice == 'h':
        printWelcomeScreen()
        print ' [INFO]: Manual opened in browser.\n'
        manualFile = 'manual' + functions.getOsSlash() + 'index.html'
        webbrowser.open('file://' + os.path.realpath(manualFile))
    elif choice == 'q':
        functions.appendLog('i', 'Application Pythronic stopped.')
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
            print ' [ ]', 'Drives settings passed.'

        if scanComputerPslist(casename, eName):
            print ' [X]', 'Process settings completed.'
        else:
            print ' [ ]', 'Process list settings passed.'

        if scanComputerNetwork(casename, eName):
            print ' [X]', 'Network settings completed.'
        else:
            print ' [ ]', 'Network settings passed.'

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

        for match in re.findall('[A-Z]{1}[:]{1}|[/]dev[/]sda[0-9]/|[/]dev[/]'
                                '[a-z]{3,4}[0-9]{0,2}[a-z]{0,2}[0-9]|[/][\']'
                                '|[/][V][a-z]{0,12}[/][A-Z]{0,12}|[N][T][F][S]'
                                '|[n][t][f][s]|[e][x][t][2-4]|[e]{0,1}[x]{0,1}'
                                '[F][A][T]|[h][f][s]|[R][e][F][S]', diskinfo):
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
        files = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]

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


def makeRapport(casename, eName, evidenceType):
    opeSysSlash = '/'

    casepath = (os.getcwd() + opeSysSlash + 'data' + opeSysSlash +
                casename + opeSysSlash)
    name = 'report_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.html'
    namef = 'report_files_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.html'

    result = False

    try:
        iconOk = ('<span class="glyphicon glyphicon-ok" aria-hidden="true">'
                  '</span>')
        iconRemove = ('<span class="glyphicon glyphicon-remove"'
                      'aria-hidden="true"></span>')

        db = sqlite3.connect(getCaseDatabase(casename))
        db2 = sqlite3.connect('db/pythronic.db')
        cursor = db.cursor()
        cursor2 = db2.cursor()

        cursor.execute('''SELECT id, name, description, type, created_at, deleted
                          FROM evidences''')
        fetchEvidences = cursor.fetchall()

        cursor.execute('''SELECT id, name, description, created_at
                          FROM general''')
        fetchGeneral = cursor.fetchall()

        cursor.execute('''SELECT id, processor, usb_devices, system_arch,
                          proc_name, proc_family, used_memory, free_memory,
                          total_memory FROM ''' + eName + '''_hardware''')
        fetchHardware = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM ''' + eName + '''_software''')
        fetchSoftware = cursor.fetchall()

        cursor.execute('''SELECT id, dropbox, onedrive, evernote, googledrive
                          FROM ''' + eName + '''_cloud''')
        fetchCloud = cursor.fetchall()

        cursor.execute('''SELECT id, his_chrome, his_ff, his_iexplorer
                          FROM ''' + eName + '''_browser''')
        fetchBrowser = cursor.fetchall()

        cursor.execute('''SELECT id, drive_name, drive_mountpoint, drive_filesystem
                           FROM ''' + eName + '''_drive''')
        fetchDrive = cursor.fetchall()

        cursor.execute('''SELECT id, name, size, shahash, md5hash
                          FROM ''' + eName + '''_files LIMIT 0, 10''')
        fetchFiles = cursor.fetchall()

        if len(fetchFiles) == 10:
            cursor.execute('''SELECT id, name, size, shahash, md5hash
                              FROM ''' + eName + '''_files''')
            fetchAllFiles = cursor.fetchall()

        cursor.execute('''SELECT html_view
                          FROM ''' + eName + '''_files_overview''')
        fetchFilesOverview = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM ''' + eName + '''_linux_logon''')
        fetchLinuxLogin = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM ''' + eName + '''_win_logon''')
        fetchWindowsLogon = cursor.fetchall()

        cursor.execute('''SELECT id, ip, mac, connected_ip
                          FROM ''' + eName + '''_network''')
        fetchNetwork = cursor.fetchall()

        cursor.execute('''SELECT id, name
                          FROM ''' + eName + '''_pslist''')
        fetchPslist = cursor.fetchall()

        cursor.execute('''SELECT id, ddate, datetime, level, description
                           FROM logs''')
        fetchLogCase = cursor.fetchall()

        cursor2.execute('''SELECT id, ddate, datetime, level, description
                           FROM logs''')
        fetchLogPythronic = cursor2.fetchall()

        #  START ALL FILES HTML

        if fetchAllFiles:
            try:
                html2 = '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8" />
                        <title>Pythronic - Rapport - Alle bestanden</title>
                        <meta name="viewport" content="width=device-width,
                        initial-scale=1.0" />
                        <link rel="stylesheet" type="text/css"
                        href="../../bootstrap/css/bootstrap.min.css" />
                        <link rel="stylesheet" type="text/css"
                        href="../../bootstrap/css/font-awesome.min.css" />
                        <script type="text/javascript"
                        src="../../bootstrap/js/jquery-1.10.2.min.js"></script>
                        <script type="text/javascript"
                        src="../../bootstrap/js/bootstrap.min.js"></script>
                    </head>
                    <body>
                    <div class="container">
                    <div class="page-header">
                        <h1>Pythronic <small>Alle bestanden</small></h1>
                    </div>
                    <div class="container">
                    <div class="alert alert-info alert-dismissible"
                    role="alert">
                    <button type="button" class="close" data-dismiss="alert">
                    <span aria-hidden="true">&times;</span>
                    <span class="sr-only">Close</span></button>
                    Dit is het automatisch gerenegeerde rapport, gemaakt op
                    ''' + time.strftime('%Y-%m-%d %H-%M-%S') + '''.
                    Bekijk de resultaten in de uitklapbare lijsten.
                    Dit rapport maakt deel uit van een ander rapport.
                    </div>
                    <div class="panel-group" id="accordion">
                    <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 class="panel-title">
                            <a class="accordion-toggle"
                            data-toggle="collapse" data-parent="#accordion"
                            href="#collapseOne"> Alle bestanden</a>
                        </h4>
                    </div>
                    <div id="collapseOne" class="panel-collapse">
                    <div class="panel-body">
                        <table class="table table-hover">
                        <tr>
                            <th>ID</th>
                            <th>Naam</th>
                            <th>Size</th>
                            <th>SHA</th>
                            <th>MD5</th>
                        </tr>
                '''

                for row in fetchAllFiles:
                    html2 += ('<tr>')
                    html2 += ('<td>{0}</td><td>{1}</td><td>{2}</td>'
                              '<td>{3}</td><td>{4}</td>'
                              .format(row[0],
                                      row[1],
                                      row[2],
                                      row[3],
                                      iconRemove if str(row[4]) == 'None'
                                      else row[4]))
                    html2 += ('</tr>')

                html2 += '''
                    </table>
                    </div>
                    </div>
                    </div>
                    </div>
                    <style>
                    .faqHeader {
                        font-size: 27px;
                        margin: 20px;
                    }

                    .panel-heading [data-toggle="collapse"]:after {
                        font-family: 'Glyphicons Halflings';
                        content: "\e072"; /* "play" icon */
                        float: right;
                        color: #F58723;
                        font-size: 18px;
                        line-height: 22px;
                        -webkit-transform: rotate(-90deg);
                        -moz-transform: rotate(-90deg);
                        -ms-transform: rotate(-90deg);
                        -o-transform: rotate(-90deg);
                        transform: rotate(-90deg);
                    }

                    .panel-heading [data-toggle="collapse"].collapsed:after {
                        -webkit-transform: rotate(90deg);
                        -moz-transform: rotate(90deg);
                        -ms-transform: rotate(90deg);
                        -o-transform: rotate(90deg);
                        transform: rotate(90deg);
                        color: #454444;
                    }
                    </style>
                    </div>
                    </body>
                    </html>
                '''

                file = open(casepath + namef, 'w')
                file.write(html2)
                file.close()
            except:
                pass

        #  END ALL FILES HTML

        #  START START HTML

        html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8" />
                <title>Pythronic - Rapport</title>
                <meta name="viewport" content="width=device-width,
                initial-scale=1.0" />
                <link rel="stylesheet" type="text/css"
                href="../../bootstrap/css/bootstrap.min.css" />
                <link rel="stylesheet" type="text/css"
                href="../../bootstrap/css/font-awesome.min.css" />
                <script type="text/javascript"
                src="../../bootstrap/js/jquery-1.10.2.min.js"></script>
                <script type="text/javascript"
                src="../../bootstrap/js/bootstrap.min.js"></script>

                <link rel="stylesheet"
                href="../../bootstrap/css/folder-tree-static.css" type="text/css">
                <link rel="stylesheet" href="../../bootstrap/css/context-menu.css"
                type="text/css">
                <script type="text/javascript" src="../../bootstrap/js/ajax.js">
                </script>
                <script type="text/javascript"
                src="../../bootstrap/js/folder-tree-static.js"></script>
                <script type="text/javascript"
                src="../../bootstrap/js/context-menu.js"></script>
            </head>
        '''

        #  END START HMLT

        #  START HTML BODY
        html += '''
            <body>
                <div class="container">
                <div class="page-header">
                    <h1>Pythronic <small>Report</small></h1>
                </div>
                <div class="container">
                <div class="alert alert-info alert-dismissible" role="alert">
                    <button type="button" class="close" data-dismiss="alert">
                    <span aria-hidden="true">&times;</span>
                    <span class="sr-only">Close</span></button>
                    Dit is het automatisch gerenegeerde rapport, gemaakt op
                    ''' + time.strftime('%Y-%m-%d %H-%M-%S') + '''.
                    Bekijk de resultaten in de uitklapbare lijsten.
                </div>
                <div class="panel-group" id="accordion">
                <div class="faqHeader">Case [''' + casename + ''']</div>
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseOne"> Bewijsmateriaal</a>
                    </h4>
                </div>
                <div id="collapseOne" class="panel-collapse collapse">
                <div class="panel-body">
                    <table class="table table-hover">
                    <tr>
                        <th>ID</th>
                        <th>Naam</th>
                        <th>Beschrijving</th>
                        <th>Type</th>
                        <th>Aangemaakt op</th>
                        <th>Verwijderd</th>
                    </tr>
        '''

        for row in fetchEvidences:
            html += ('<tr>')
            html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                     '<td>{4}</td><td>{5}</td>'
                     .format(row[0],
                             row[1],
                             row[2] if row[2] != '' else '-',
                             'PC / Laptop / Server' if str(row[3]) == '1'
                             else 'Device (USB, SD, HDD)',
                             row[4],
                             'Ja' if str(row[5]) == '1' else 'Nee'))
            html += ('</tr>')

        html += '''
            </table>
            </div>
            </div>
            </div>
            <div class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a class="accordion-toggle collapsed"
                    data-toggle="collapse" data-parent="#accordion"
                    href="#collapseTwo">Algemeen</a>
                </h4>
            </div>
            <div id="collapseTwo" class="panel-collapse collapse">
            <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                    <th>Beschrijving</th>
                    <th>Aangemaakt op</th>
                </tr>
        '''

        for row in fetchGeneral:
            html += ('<tr>')
            html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                     .format(row[0],
                             row[1],
                             row[2] if row[2] != '' else '-',
                             row[3]))
            html += ('</tr>')

        html += '''
            </table>
            </div>
            </div>
            </div>
            <div class="faqHeader">Modules</div>
        '''

        #  END BODY HTML
        #  START IF HARDWARE

        if fetchHardware and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseThree">Hardware info</a>
                    </h4>
                </div>
                <div id="collapseThree" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>CPU</th>
                    <th>USB Devices</th>
                    <th>Architectuur</th>
                    <th>CPU Naam</th>
                    <th>CPU Family</th>
                    <th>Gebruikte Geheugen</th>
                    <th>Vrije Geheugen</th>
                    <th>Totaal Geheugen</th>
                </tr>
            '''

            for row in fetchHardware:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         '<td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td>'
                         '<td>{8}</td>'
                         .format(row[0],
                                 iconRemove if str(row[1]) == 'None'
                                 else row[1],
                                 iconRemove if str(row[2]) == 'None'
                                 else row[2],
                                 iconRemove if str(row[3]) == 'None'
                                 else row[3],
                                 iconRemove if str(row[4]) == 'None'
                                 else row[4],
                                 iconRemove if str(row[5]) == 'None'
                                 else row[5],
                                 iconRemove if str(row[6]) == 'None'
                                 else row[6],
                                 iconRemove if str(row[7]) == 'None'
                                 else row[7],
                                 iconRemove if str(row[8]) == 'None'
                                 else row[8]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF HARDWARE
        #  START IF SOFTWARE

        if fetchSoftware and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseFour">Software lijst</a>
                    </h4>
                </div>
                <div id="collapseFour" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchSoftware:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0], row[1].encode('utf-8')))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF SOFTWARE
        #  START IF CLOUD

        if fetchCloud and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseFive">Cloud gebruik</a>
                    </h4>
                </div>
                <div id="collapseFive" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Dropbox</th>
                    <th>OneDrive</th>
                    <th>Evernote</th>
                    <th>Google Drive</th>
                </tr>
            '''

            for row in fetchCloud:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td>'
                         '<td>{3}</td><td>{4}</td>'
                         .format(row[0],
                                 iconOk if str(row[1]) == '1' else iconRemove,
                                 iconOk if str(row[2]) == '1' else iconRemove,
                                 iconOk if str(row[3]) == '1' else iconRemove,
                                 iconOk if str(row[4]) == '1' else iconRemove))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF CLOUD
        #  START IF BROWSER

        if fetchBrowser and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseSix">Browser history</a>
                    </h4>
                </div>
                <div id="collapseSix" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Chrome</th>
                    <th>FireFox</th>
                    <th>Internet Explorer</th>
                </tr>
            '''

            for row in fetchBrowser:
                iconCh = ('<a href="data' + opeSysSlash + casename +
                          opeSysSlash + eName + opeSysSlash +
                          'Chrome_History">' + iconOk + '</a>')
                iconFf = ('<a href="data' + opeSysSlash + casename +
                          opeSysSlash + eName + opeSysSlash +
                          'frfox_places.sqlite">' + iconOk + '</a>')

                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         .format(row[0],
                                 iconCh if str(row[1]) == '1' else iconRemove,
                                 iconFf if str(row[2]) == '1' else iconRemove,
                                 iconOk if str(row[3]) == '1'
                                 else iconRemove,))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>'''

        #  END IF BROWSER
        #  START IF DRIVES

        if fetchDrive and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseSeven">Detected drives</a>
                    </h4>
                </div>
                <div id="collapseSeven" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Drive Naam</th>
                    <th>Drive Mount</th>
                    <th>Drive filesystem</th>
                </tr>
            '''

            for row in fetchDrive:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         .format(row[0],
                                 row[1],
                                 row[2],
                                 row[3]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF DRIVES
        #  START IF FILE HASH

        if fetchFiles:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseEight">File hashing</a>
                    </h4>
                </div>
                <div id="collapseEight" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
            '''

            if len(fetchFiles) == 10:
                message = ('<b>Info</b>: Er bevinden zich meer dan 10 '
                           'bestanden in de database. Er worden er hieronder '
                           '10 getoond. <a href="' + casepath + namef + '">'
                           'Klik hier</a> om alle bestanden te zien.')

                html += '''
                    <div class="alert alert-success alert-dismissible"
                    role="alert"><button type="button" class="close"
                    data-dismiss="alert"><span aria-hidden="true">&times;
                    </span><span class="sr-only">Close</span></button>
                        ''' + message + '''
                    </div>
                '''

            html += '''
                <tr>
                    <th>ID</th>
                    <th>Bestandsnaam</th>
                    <th>Size</th>
                    <th>SHA</th>
                    <th>MD5</th></tr>
            '''

            for row in fetchFiles:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td>'
                         '<td>{3}</td><td>{4}</td>'
                         .format(row[0],
                                 row[1],
                                 row[2],
                                 row[3],
                                 iconRemove if str(row[4]) == 'None'
                                 else row[4]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF FILE HASH
        #  IF FILE HIERARCHY

        if fetchFilesOverview:
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseEightB">File hiarchie</a>
                    </h4>
                </div>
                <div id="collapseEightB" class="panel-collapse collapse">
                <div class="panel-body">
            '''

            for row in fetchFilesOverview:
                html += row[0]

            html += '''
                </div>
                </div>
                </div>
            '''

        #  END FILE HIERARCHY
        #  IF LINUX LOGON

        if fetchLinuxLogin and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseNine">Linux login items</a>
                    </h4>
                </div>
                <div id="collapseNine" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchLinuxLogin:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0], row[1]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF LINUX LOGON
        #  START WINDOWS LOGON

        if fetchWindowsLogon and evidenceType == '1':
            html == '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseEleven">Windows startup applications</a>
                    </h4>
                </div>
                <div id="collapseEleven" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchWindowsLogon:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0],
                                 row[1]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF LINUX LOGON
        #  START IF NETWORK

        if fetchNetwork and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseThirteen">Networking details</a>
                    </h4>
                </div>
                <div id="collapseThirteen" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>IP</th>
                    <th>MAC</th>
                    <th>IP Connected</th>
                </tr>
            '''

            for row in fetchNetwork:
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                         .format(row[0], row[1],
                                 iconRemove if str(row[2]) == 'None'
                                 else row[2],
                                 iconRemove if str(row[3]) == 'None'
                                 else row[3]))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF NETWORK
        #  START IF PSLIST

        if fetchPslist and evidenceType == '1':
            html += '''
                <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a class="accordion-toggle collapsed"
                        data-toggle="collapse" data-parent="#accordion"
                        href="#collapseThirteenB">Processen</a>
                    </h4>
                </div>
                <div id="collapseThirteenB" class="panel-collapse collapse">
                <div class="panel-body">
                <table class="table table-hover">
                <tr>
                    <th>ID</th>
                    <th>Naam</th>
                </tr>
            '''

            for row in fetchPslist:
                boundName = '[bound method Process.name of ['
                i = str(row[1]).encode('utf-8')
                process = i.replace('<', '[')
                process = process.replace('>', ']')
                process = process.replace(boundName, '')
                process = process.replace(']]', '')
                html += ('<tr>')
                html += ('<td>{0}</td><td>{1}</td>'
                         .format(row[0], process))
                html += ('</tr>')

            html += '''
                </table>
                </div>
                </div>
                </div>
            '''

        #  END IF PSLIST
        #  START LOGGING

        html += '''
            <div class="faqHeader">Logging</div>
            <div class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a class="accordion-toggle collapsed"
                    data-toggle="collapse" data-parent="#accordion"
                    href="#collapseLogOne">Case logging</a>
                </h4>
            </div>
            <div id="collapseLogOne" class="panel-collapse collapse">
            <div class="panel-body">
            <table class="table table-hover">
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Timestamp</th>
                <th>Level</th>
                <th>Omschrijving</th>
            </tr>
        '''

        for row in fetchLogCase:
            html += ('<tr>')
            html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                     '<td>{4}</td>'
                     .format(row[0], row[1], row[2],
                             'warning' if str(row[3]) == 'w'
                             else 'info',
                             row[4]))
            html += ('</tr>')

        html += '''
            </table>
            </div>
            </div>
            </div>
        '''

        html += '''
            <div class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a class="accordion-toggle collapsed"
                    data-toggle="collapse" data-parent="#accordion"
                    href="#collapseLogTwo">Pythronic logging</a>
                </h4>
            </div>
            <div id="collapseLogTwo" class="panel-collapse collapse">
            <div class="panel-body">
            <table class="table table-hover">
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Timestamp</th>
                <th>Level</th>
                <th>Omschrijving</th>
            </tr>
        '''

        for row in fetchLogPythronic:
            html += ('<tr>')
            html += ('<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'
                     '<td>{4}</td>'
                     .format(row[0], row[1], row[2],
                             'warning' if str(row[3]) == 'w'
                             else 'info',
                             row[4]))
            html += ('</tr>')

        html += '''
            </table>
            </div>
            </div>
            </div>
        '''

        #  END LOGGING
        #  START BAR STYLING

        html += '''
            <style>
                .faqHeader {
                    font-size: 27px;
                    margin: 20px;
                }

                .panel-heading [data-toggle="collapse"]:after {
                    font-family: 'Glyphicons Halflings';
                    content: "\e072"; /* "play" icon */
                    float: right;
                    color: #F58723;
                    font-size: 18px;
                    line-height: 22px;
                    /* rotate "play" icon from > (right arrow) to down arrow */
                    -webkit-transform: rotate(-90deg);
                    -moz-transform: rotate(-90deg);
                    -ms-transform: rotate(-90deg);
                    -o-transform: rotate(-90deg);
                    transform: rotate(-90deg);
                }

                .panel-heading [data-toggle="collapse"].collapsed:after {
                    -webkit-transform: rotate(90deg);
                    -moz-transform: rotate(90deg);
                    -ms-transform: rotate(90deg);
                    -o-transform: rotate(90deg);
                    transform: rotate(90deg);
                    color: #454444;
                }
            </style>
        '''

        #  END BAR STYLING
        #  START END HTML

        html += '''
            </div>
            </body>
            </html>
        '''

        #  END END HTML

        file = open(casepath + name, 'w')
        file.write(html)
        file.close()

        print '\n [INFO]: Report created. Path: ' + casepath + namef + '.\n'

        result = True
    except:
        pass

    return result


#  END SCAN ITEMS


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
