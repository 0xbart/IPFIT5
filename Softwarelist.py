from _winreg import *
import os
import win32api

softwarelist = []

# Search first registry

def read_first_registry():
    uninstall = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(uninstall,
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    for i in range(1024):
        try:
            keyname = EnumKey(regcontent, i)
            regdata = OpenKey(regcontent, keyname)
            entries = QueryValueEx(regdata, "DisplayName")
            softwarelist.append(entries)
        except WindowsError:
            pass

# Search second registry


def read_second_registry():
    uninstall = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(uninstall,
    r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
    for i in range(1024):
        try:
            keyname = EnumKey(regcontent, i)
            asubkey = OpenKey(regcontent, keyname)
            entries = QueryValueEx(asubkey, "DisplayName")
            softwarelist.append(entries)
        except WindowsError:
            pass
    print "These programs are recorded in the registry (for this user only) :"
    list(set(softwarelist))
    print softwarelist

read_first_registry()
read_second_registry()
