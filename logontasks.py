__author__ = 'Michael'

from winreg import *

print (r"*** Reading from registry SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***")
aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
for i in range(1024):
    try:
        n,v,t = EnumValue(aKey,i)
        print (i, n, v, t)
    except EnvironmentError:
        print ("You have",i,"tasks starting at logon.")
        break

CloseKey(aKey)


