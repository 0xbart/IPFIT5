import shutil
import sys
import os
import os.path

# Input name for the machine
name = input("Username of the PC required: ")

# Simple menu printing the different options
print("\n" + "Make a choice: " + "\n"  + "1: Google Chrome\n" + "2: Internet Explorer\n" + "3: Firefox" + "\n" + "0: Exit program" + "\n")

# Loop for a correct input of the user
correct = False
while not correct:
    try:
        browserInput = int(input("Which browser history would you like to retrieve? "))
        correct = True
    except ValueError:
        print("Invalid value, please pick a number from the list")

# Destination folder for the file to be transfered, if the folder does not exists, it will create one.
dest = input("Destination folder: ")
if not os.path.exists(dest):
    os.mkdir(dest)

# Input handling of the user
def browser():
    if browserInput == 1:
        chrome()
    elif browserInput == 2:
        IE()
    elif browserInput == 3:
        firefox()
    elif browserInput == 0:
        print("Proces terminated")
        sys.exit()

# Chrome function that locates the history files
def chrome():
    try:
        chrome = ("C:\\Users\%s\AppData\Local\Google\Chrome\\User Data\Default\History" % name)
        shutil.copy2(chrome, dest)
    except IOError:
        print("Sorry, could not locate the Google Chrome files" + "\n" + "Did you use the correct username?")

# IE function that located the history files, at 3 different locations.
def IE():
    try:
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name)
            shutil.copy2(internet, dest)
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name)
            shutil.copy2(internet, dest)
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name)
            shutil.copy2(internet, dest)
        else:
            print("Sorry, could not locate the IE files" + "\n" + "Did you use the correct username?")
    except IOError:
        print("Sorry, could not locate the IE files" + "\n" + "Did you use the correct username?")

# Firefox function that locates the firefox files.
def firefox():
    try:
        osfirefox = os.listdir("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles" % name)
        osfirefoxformat = (str(osfirefox)[2:-2])
        firefox = ("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles\%s\places.sqlite" % (name, osfirefoxformat))
        shutil.copy2(firefox, dest)
    except IOError:
        print("Sorry, could not locate the Firefox files" + "\n" + "Did you use the correct username?")

browser()