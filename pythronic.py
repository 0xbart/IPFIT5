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
userID = None
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
        print (' [INFO]: Database doesn\'t exist; executing setup.\n')
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

    cow1 = ' ---------------------- '
    cow2 = '  WELCOME TO PYTHRONIC '
    cow3 = ' ---------------------- '
    cow4 = '             \   ^__^'
    cow5 = '              \  (oo)\_______'
    cow6 = '                 (__)\       )\/\\'
    cow7 = '                     ||----w |'
    cow8 = '                     ||     ||'

    print ''
    print cow1
    print cow2
    print cow3
    print cow4
    print cow5
    print cow6
    print cow7
    print cow8

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


def newCase():
    result = False
    printWelcomeScreen()
    while True:
        print ' Creating new case\n'
        name = functions.askInput('Enter name case', 's')
        desc = functions.askInput('Enter description case', 's')
        if name.isalpha():
            if functions.createCase(name, desc, user):
                print (' [INFO]: Case succesfully created.')
                result = functions.getCaseID(name)
                break
        else:
            print '\n [ERROR]: Name must be an alphabetic string, no spaces.\n'
    return result


def getCase():
    printWelcomeScreen()
    while True:
        print ' 1. New case\n 2. Load case\n 3. Delete case\n 4. Manage users'
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
                    print ' User succesfully added to the database.\n\n'
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
                if not functions.checkUserExist(username):
                    break
                else:
                    print '\n [ERROR]: Username exist, try another name.\n'
            password = functions.askInput('Enter password', 's')
            if functions.createUser(username, password):
                result = True
                break
            else:
                print '\n [ERROR]: User cannot be created!\n'
                break
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
                        break
                    else:
                        print '\n You cannot delete yourself!\n'
                else:
                    print '\n Wrong input, try again!\n'
        else:
            print '\n [ERROR]: No other users found.\n'
    return result


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
            evidences = functions.getEvidences(casename)
            if len(evidences) > 0:
                evidenceIDs = functions.getEvidenceIDs(casename)
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
                            if functions.deleteEvidence(casename, str(choice), confirm.lower()):
                                # printWelcomeScreen()
                                print ' [INFO]: Evidence ' + evidence + ' deleted succesfully!\n'
                                break
                            else:
                                # printWelcomeScreen()
                                print ' [ERROR]: Evidence ' + evidence + ' cannot be deleted!\n'
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
            print 'scan starten...'
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
            if not etype in evidenceTypes:
                printWelcomeScreen()
                print ' [ERROR]: EvidenceType is not a valid choice.\n'
            else:
                printWelcomeScreen()
                print ' [ERROR]: Name must be an alphabetic string, no spaces.\n'
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


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
