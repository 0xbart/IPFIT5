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

opeSys = False
opeSysSlash = False


def main():
    detectOs()
    printWelcomeScreen()
    startApplication()


def startApplication():
    if not os.path.isfile("./db/pythronic.db"):
        setup.createDatabase()


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

    # message = '######################\n\n'
    # message += ' Welcome by Pytronic! \n\n'
    # message += '######################\n'

    message = '\n Welcome by Pytronic! \n\n'

    return print (message)


def clearScreen():
    global opeSys

    if opeSys == "linux" or opeSys == "osx":
        os.system("clear")
    elif opeSys == "windows":
        os.system("cls")


main()
