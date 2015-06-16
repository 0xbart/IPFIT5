from _winreg import *
import os
import win32api

softwarelist = []

#Search executables
def programfiles():
    print("What drive is Windows installed on?")
    drives = win32api.GetLogicalDriveStrings()
    print (drives)
    disk = raw_input()
    walklist = []
    path = disk + ":\Program Files (x86)\\"
    walklist.append(path)
    path = disk + ":\Program Files\\"
    walklist.append(path)
    dirlist = []
    exelist = []

    for i in walklist:
        try:
            dirs = os.listdir(i)
            for file in dirs:
                dirlist.append(i + file + "\\")
                dirlist.sort()
        except WindowsError:
            print "Could not resolve path, are you sure this is the right drive?"

    for i in dirlist:
        try:
            filefind = os.listdir(i)
            for file in filefind:
                if file.endswith('.exe'):
                    exelist.append(file)
                    exelist.sort()
        except WindowsError:
            print "Could not resolve path"
    print exelist
programfiles()
#Search first registry
def readfirst():
    uninstall = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(uninstall, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    for i in range(1024):
        try:
            keyname = EnumKey(regcontent, i)
            regdata = OpenKey(regcontent, keyname)
            entries = QueryValueEx(regdata, "DisplayName")
            softwarelist.append(entries)
            print softwarelist
        except WindowsError:
            pass

#Search second registry
def readsecond():
    uninstall = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(uninstall, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
    for i in range(1024):
        try:
            keyname = EnumKey(regcontent, i)
            asubkey = OpenKey(regcontent, keyname)
            entries = QueryValueEx(asubkey, "DisplayName")
            softwarelist.append(entries)
            print softwarelist
        except WindowsError:
            pass
