import shutil
import sys
import os
import os.path
import glob
from sys import platform as _platform
import sqlite3
import getpass
import pythronic

name = getpass.getuser()
his_iexplorer = 0
his_ff = 0
his_chrome = 0
dest = "Data"
if not os.path.exists(dest):
    os.mkdir(dest)
# Destination folder for the file to be transfered, if the folder does not exists, it will create one.

print his_ff

	
# Chrome function that locates the history files
def chrome_win():
    try:
        chrome = ("C:\\Users\%s\AppData\Local\Google\Chrome\User Data\Default\History" % name)
        shutil.copy2(chrome, dest)
        global his_chrome 
        his_chrome = 1
    except IOError:
        pass


def chrome_linux():
    try:
        chrome = ("/home/%s/.config/google-chrome/Default/History" % name)
        shutil.copy2(chrome, dest)
        global his_chrome
        his_chrome = 1
    except:
        pass

def chrome_osx():
    try:
        chrome = ("/Users/%s/Library/Application Support/Google/Chrome/Default//History" % name)
        shutil.copy2(chrome, dest)
        global his_chrome
        his_chrome = 1
    except:
        pass

def IE():
    try:
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Internet Explorer\IECompatData\\" % name)
            shutil.copy2(internet, dest)
            global his_iexplorer
            his_iexplorer = 1
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\History\\" % name)
            shutil.copy2(internet, dest)
            his_iexplorer = 1 
        if os.path.isfile("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name):
            internet = ("C:\\Users\%s\AppData\Local\Microsoft\Windows\WebCache\\" % name)
            shutil.copy2(internet, dest)
            his_iexplorer = 1
    except IOError:
        pass

# Firefox function that locates the firefox files.
def firefox_win():
    try:
        osfirefox = os.listdir("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\\Profiles" % name)
        osfirefoxformat = (str(osfirefox)[2:-2])
        firefox = ("C:\\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles\%s\\places.sqlite" % (name, osfirefoxformat))
        shutil.copy2(firefox, dest)
        global his_ff
        his_ff = 1
    except IOError:
        pass 

def firefox_linux():
    try:
        os.chdir("/home/%s/.mozilla/firefox" % name)
        for file in glob.glob("*.default"):
            firefox = ("/home/%s/.mozilla/firefox/%s/places.sqlite" % (name, file))
            shutil.copy2(firefox, dest)
            global his_ff
            his_ff = 1
    except:
        pass 

def firefox_osx():
    try:
        os.chdir("/Users/%s/Library/Application Support/Firefox/Profiles" % name)
        for file in glob.glob("*.default"):
            firefox = ("/Users/%s/Library/Application Support/Firefox/Profiles/%s/places.sqlite" % (name, file))
            shutil.copy2(firefox, dest)
            global his_ff
            his_ff = 1
    except:
        pass

def scanComputerHistory(casename, eName):
    # Input name for the machine
    dest = "Data"
    if not os.path.exists(dest):
        os.mkdir(dest)

    if _platform == 'win32':
        IE()
        chrome_win()
        firefox_win()
        print his_chrome
        print his_ff
        print his_iexplorer
    elif _platform == "linux" or _platform == "linux2":
        chrome_linux()
        firefox_linux()
		
    elif _platform == "darwin":
        chrome_osx()
        firefox_osx()
	
	db = sqlite3.connect(pythronic.getCaseDatabase(casename))
	cursor = db.cursor()
	cursor.execute('INSERT INTO `' + eName + '_browser` ('
	'his_chrome, his_ff, his_iexplorer) '
	'VALUES (?,?,?)', (
	his_chrome, his_ff, his_iexplorer))
	
	db.commit()

scanComputerHistory('cloud', 'laptop')