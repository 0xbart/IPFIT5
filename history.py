import shutil
import sys
import os
import os.path
import glob
from sys import platform as _platform
# Input name for the machine
name = raw_input("Username of the PC required: ")

# Simple menu printing the different options
print("\n" + "Make a choice: " + "\n"  + "1: Google Chrome\n" + "2: Internet Explorer\n" + "3: Firefox" + "\n" + "0: Exit program" + "\n")

# Loop for a correct input of the user
# Destination folder for the file to be transfered, if the folder does not exists, it will create one.


# Input handling of the user
def browser_menu():
    global dest
    try:
        browserInput = raw_input("Which browser history would you like to retrieve? ")
    except ValueError:
        print("Invalid value, please pick a number from the list")

    dest = raw_input("Destination folder: ")
    if not os.path.exists(dest):
        os.mkdir(dest)

    if browserInput == "1":
        if _platform == 'win32':
            chrome_win()
        elif _platform == "linux" or _platform == "linux2":
            chrome_linux()
        elif _platform == "darwin":
            chrome_osx()
    elif browserInput == "2":
        if _platform == 'win32':
            IE()
        elif _platform == "linux" or _platform == "linux2" or _platform == "darwin":
            print("Internet Explorer is not supported on Unix or OSX systems.")
    elif browserInput == "3":
        if _platform == 'win32':
            firefox_win()
        elif _platform == "linux" or _platform == "linux2":
            firefox_linux()
        elif _platform == "darwin":
            firefox_osx()

    elif browserInput == 0:
        print("Proces terminated")
        sys.exit()

# Chrome function that locates the history files
def chrome_win():
    try:
        chrome = ("C:\\Users\%s\AppData\Local\Google\Chrome\User Data\Default\History" % name)
        shutil.copy2(chrome, dest)
    except IOError:
        print("Sorry, could not locate the Google Chrome files" + "\n" + "Did you use the correct username?")


def chrome_linux():
    try:
        chrome = ("/home/%s/.config/google-chrome/Default/History" % name)
        shutil.copy2(chrome, dest)
        print(chrome)
    except:
        print("Sorry, could not locate the Google Chrome files" + "\n" + "Did you use the correct username?")

def chrome_osx():
    try:
        chrome = ("/Users/%s/Library/Application Support/Google/Chrome/Default//History" % name)
        shutil.copy2(chrome, dest)
        print(chrome)
    except:
        print("Sorry, could not locate the Google Chrome files" + "\n" + "Did you use the correct username?")

def IE():
    try:
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name)
            shutil.copy2(internet, dest)
            print("1")
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name)
            shutil.copy2(internet, dest)
            print("2")
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name)
            shutil.copy2(internet, dest)
            print("3")
        else:
            print("Sorry, could not locate the IE files" + "\n" + "Did you use the correct username?")
    except IOError:
        print("Sorry, could not locate the IE files" + "\n" + "Did you use the correct username?")

# Firefox function that locates the firefox files.
def firefox_win():
    try:
        osfirefox = os.listdir("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\\Profiles" % name)
        osfirefoxformat = (str(osfirefox)[2:-2])
        firefox = ("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles\%s\\places.sqlite" % (name, osfirefoxformat))
        shutil.copy2(firefox, dest)
    except IOError:
        print("Sorry, could not locate the Firefox files" + "\n" + "Did you use the correct username?")

def firefox_linux():
    try:
        os.chdir("/home/%s/.mozilla/firefox" % name)
        for file in glob.glob("*.default"):
            firefox = ("/home/%s/.mozilla/firefox/%s/places.sqlite" % (name, file))
            shutil.copy2(firefox, dest)
    except:
        print("Sorry, could not locate the Firefox files" + "\n" + "Did you use the correct username?")

def firefox_osx():
    try:
        os.chdir("/Users/%s/Library/Application Support/Firefox/Profiles" % name)
        for file in glob.glob("*.default"):
            firefox = ("/Users/%s/Library/Application Support/Firefox/Profiles/%s/places.sqlite" % (name, file))
            shutil.copy2(firefox, dest)
    except:
        print("Sorry, could not locate the Firefox files" + "\n" + "Did you use the correct username?")

browser_menu()