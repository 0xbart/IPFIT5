"""
    IPFIT5 - Hogeschool Leiden

    Contributers:
    - Michael van Huis
    - Chester van den Bogaard
    - Welsey Boumans
    - Bart Mauritz
"""
from sys import platform as _platform
import setup
import os
import functions

opeSys      = False
opeSysSlash = False
user        = False
case        = False


def main():
    detectOs()
    printWelcomeScreen()
    startApplication()
    login()
    getCase()
    menu()


def startApplication():
    if not os.path.isfile("./db/pythronic.db"):
        print (" [ERROR]: Database doesn't exist; executing setup.\n")
        setup.createDatabase()
        printWelcomeScreen()


def detectOs():
    global opeSys
    global opeSysSlash

    if _platform == "linux" or _platform == "linux2":
        opeSys = "linux"
        opeSysSlash = "/"
    elif _platform == "darwin":
        opeSys = "osx"
        opeSysSlash = "/"
    elif _platform == "win32":
        opeSys = "windows"
        opeSysSlash = "\\"

    return opeSys


def printWelcomeScreen():
    clearScreen()
    message = '\n'
    message += ' Welcome by Pytronic! \n\n'
    return print (message)


def clearScreen():
    global opeSys

    if opeSys == "linux" or opeSys == "osx":
        os.system("clear")
    elif opeSys == "windows":
        os.system("cls")


def login():
    print (' Login first:\n')
    username = input(" Username: ")
    password = input(" Password: ")
    authUser = username

    while (functions.checkLogin(username, password)):
        print ('\n Login failed, try again: \n')
        username = input(" Username: ")
        password = input(" Password: ")
        if not functions.checkLogin(username, password):
            authUser = username

    global user
    user = authUser
    return user


def getCase():
    printWelcomeScreen()
    while True:
        print (' 1. New case\n 2. Load case')
        choice = int(input('\n Make a choice: '))
        if choice == 1:
            print (" You entered new case!")
            break
        elif choice == 2:
            cases = functions.getCases()
            if len(cases) > 0:
                loadCase(cases)
                break
            else:
                print ("\n No cases found in the database.\n")
        else:
            print (" \nWrong input, try again!\n")


def loadCase(cases):
    printWelcomeScreen()
    casesNumbers = functions.getCasesNumbers()
    print (" Following cases are found:\n")
    while True:
        for case in cases:
            print(' {0}: {1}'.format(case[0], case[1]))
        choice = int(input('\n Select case: '))
        if choice in casesNumbers:
            global case
            case = choice
            return case
        else:
            print ("\n Wrong input, try again!\n")


def menu():
    printWelcomeScreen()
    print (" Welcome ", user, ",\n\n Your casenumber: ", case)


if __name__ == "__main__":
    main()
