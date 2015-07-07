from _winreg import *
import os
import win32api
import sqlite3
import pythronic

softwarelist = []

# Search first registry


def scanComputerSoftware(casename, eName):

    uninstall = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(uninstall, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    for i in range(1024):
        try:
            keyname = EnumKey(regcontent, i)
            regdata = OpenKey(regcontent, keyname)
            entries = QueryValueEx(regdata, "DisplayName")
            softwarelist.append(entries)
        except WindowsError:
            pass

# Search second registry

    uninstall = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(uninstall, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
    for i in range(1024):
        try:
            keyname = EnumKey(regcontent, i)
            asubkey = OpenKey(regcontent, keyname)
            entries = QueryValueEx(asubkey, "DisplayName")
            softwarelist.append(entries)
        except WindowsError:
            pass
    uniquelist = list(set(softwarelist))
    uniquelist.sort()

    for i in uniquelist:
		db = sqlite3.connect(pythronic.getCaseDatabase(casename))
		cursor = db.cursor()
		cursor.execute('INSERT INTO `' + eName + '_software` ('
			'name) '
			'VALUES (?,?)', (
			i))
		db.commit()
		
scanComputerSoftware('cloud', 'laptop')