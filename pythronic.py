"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz
"""
from sys import platform as _platform
import os
import setup
import sys
import functions
import signal

opeSys      = None
opeSysSlash = None
user        = None
casenr      = None

def main():
    detectOs()
    startApplication()
    login()
    getCase()
    menu()


def startApplication():
    if not os.path.isfile('./db/pythronic.db'):
        print (' [ERROR]: Database doesn\'t exist; executing setup.\n')
        setup.createDatabase()
    printWelcomeScreen()


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
    message = '\n'
    message += ' Welcome by Pytronic! \n\n'
    print message


def clearScreen():
    global opeSys

    if opeSys == 'linux' or opeSys == 'osx':
        os.system('clear')
    elif opeSys == 'windows':
        os.system('cls')


def login():
    print ' Login first:\n'
    username = functions.askInput('Enter username', 's')
    password = functions.askInput('Enter password', 's')

    global user
    user = None

    while (functions.checkLogin(username, password)):
        print '\n Login failed, try again. \n'
        username = functions.askInput('Enter username', 's')
        password = functions.askInput('Enter password', 's')
        if not functions.checkLogin(username, password):
            user = username

    return user


def newCase():
    printWelcomeScreen()
    while True:
        print ' Creating new case\n'
        name = functions.askInput('Enter name case', 's')
        desc = functions.askInput('Enter description case', 's')
        if name.isalpha():
            print 'check 1'
            if functions.createCase(name, desc, user):
                print 'check 2'
                print (' [Info]: Case succesfully created.')
                return True
        else:
            print '\n [Error]: Name can only be alphabetic.\n'
    return False


def getCase():
    printWelcomeScreen()
    while True:
        print ' 1. New case\n 2. Load case\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 1:
            new = newCase()
            if new:
                break
            else:
                print '\n Error while creating new case'
        elif choice == 2:
            cases = functions.getCases()
            if len(cases) > 0:
                loadCase(cases)
                break
            else:
                print '\n No cases found in the database.\n'
        else:
            print '\n Wrong input, try again!\n'


def loadCase(cases):
    printWelcomeScreen()
    casesNumbers = functions.getCasesNumbers()
    print ' Following cases are found:\n'
    while True:
        for case in cases:
            print(' {0}: {1}'.format(case[0], case[1]))
        choice = int(input('\n Select case: '))
        if choice in casesNumbers:
            global casenr
            casenr = choice
            return casenr
        else:
            print '\n Wrong input, try again!\n'


def menu():
    printWelcomeScreen()
    print ' Welcome ', user, ',\n\n Your casenumber: ', casenr


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
