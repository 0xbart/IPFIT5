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
import webbrowser

opeSys = None
opeSysSlash = None
user = None
casenr = None
casename = None


def __init__():
    # Refactor
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
        print (' []: Database doesn\'t exist; executing setup.\n')
        setup.createDatabase()

    functions.appendLog('i', 'Application Pythronic started.')
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
    message += ' WELCOME BY PYTHRONIC! \n\n'

    if user:
        message += ' Welcome ' + str(user) + '.\n'

    if casenr:
        message += ' Casenumber: ' + str(casenr) + '.\n'
        message += ' Casename: ' + str(casename) + '.\n'

    message += '\n ###########################################\n\n'

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
    user = None

    while True:
        username = functions.askInput('Enter username', 's')
        password = functions.askInput('Enter password', 's')

        if functions.checkLogin(username, password):
            user = username
            break
        else:
            print '\n Login failed, try again. \n'

    return user


def newCase():
    result = False
    printWelcomeScreen()
    while True:
        print ' Creating new case\n'
        name = functions.askInput('Enter name case', 's')
        desc = functions.askInput('Enter description case', 's')
        if name.isalpha():
            if functions.createCase(name, desc, user):
                print (' [Info]: Case succesfully created.')
                result = functions.getCaseID(name)
                break
        else:
            print '\n []: Name can only be alphabetic.\n'
    return result


def getCase():
    printWelcomeScreen()
    while True:
        print ' 1. New case\n 2. Load case\n 3. Delete case\n\n h. Open FAQ\n q. Quit Pythronic\n'
        choice = functions.askInput('Make a choice', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice == 1:
            new = newCase()
            if new:
                details = getCaseDetails(new)
                if details:
                    break
            else:
                print '\n  while creating new case'
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
        else:
            print '\n Wrong input, try again!\n'


def manageCase(cases, action):
    printWelcomeScreen()
    casesNumbers = functions.getCasesNumbers()
    casenr = None

    print ' Following cases are found:\n'

    while True:
        for case in cases:
            print(' {0}: {1}'.format(case[0], case[1]))
        choice = functions.askInput('\n Select case', 'i')
        if choice == 'q' or choice == 'h':
            globalOperators(choice)
        elif choice in casesNumbers:
            details = getCaseDetails(choice)
            if action == 'select':
                if details:
                    casenr = choice
                    break
            elif action == 'delete':
                question = '[WARNING]: Deleting `' + casename + '`? '
                question += 'Y = yes, P = permanently, other keys = abort'
                confirm = functions.askInput(question, 's')
                if confirm.lower() == 'y' or confirm.lower() == 'p':
                    functions.deleteCase(str(choice), confirm.lower())
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
        print ' []: Cannot get case details.'

    return result


def clearCaseDetails():
    global casenr
    global casename
    casenr = None
    caseName = None

    return True


def menu():
    printWelcomeScreen()
    print ' Welcome in the menu!'


def globalOperators(choice):
    if choice == 'h':
        print ' [INFO]: FAQ opened in browser.'
        FAQfile = 'FAQ' + functions.getOsSlash() + 'index.html'
        webbrowser.open('file://' + os.path.realpath(FAQfile))
    elif choice == 'q':
        sys.exit(0)


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
