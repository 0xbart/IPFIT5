import shutil
import sys
import os
import os.path

# Input name for the machine
name = input("Username of the PC required: ")

print("\n" + "Make a choice: " + "\n"  + "1: Google Chrome\n" + "2: Internet Explorer\n" + "3: Firefox" + "\n" + "0: Exit program" + "\n")
browserInput = int(input("Which browser history would you like to retrieve? "))

# Solution for ambigious file names in firefox profile data
osfirefox = os.listdir("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles" % name)
osfirefoxformat = (str(osfirefox)[2:-2])

# Config paths for default history settings
chrome = ("C:\\Users\%s\AppData\Local\Google\Chrome\\User Data\Default\History" % name)
firefox = ("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles\%s\places.sqlite" % (name, osfirefoxformat))

# Destination folder for the file to be transfered
dest = input("Destination folder: ")

def browser():
    if browserInput == 1:
        shutil.copy2(chrome, dest)
    elif browserInput == 2:
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name)
            shutil.copy2(internet, dest)
        elif os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name)
            shutil.copy2(internet, dest)
        elif os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name)
            shutil.copy2(internet, dest)
        else:
            print("Else")
    elif browserInput == 3:
        shutil.copy2(firefox, dest)
    else:
        print("Invalid input, proces terminated")
        sys.exit()

browser()