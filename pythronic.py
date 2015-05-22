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


def main():
    detectOs()
    printWelcomeScreen()
    startApplication()
    login()
    getCase()


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


def menu():
    printWelcomeScreen()
    print ('\n Welcome ', user, ', make a choice:\n\n')
    print ('menu item 1')
    print ('menu item 2')
    print ('menu item 3')


if __name__ == "__main__":
    main()
