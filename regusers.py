from _winreg import *

print (r"*** Reading from SOFTWARE\Microsoft\WindowsNT\CurrentVersion\ProfileList ***")
aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList")
for i in range(1024):
    try:
        print (QueryInfoKey(aReg))
        n,v,t = EnumValue(aKey,i)
        print (i, n, v)
    except EnvironmentError:
        print ("You have", i, "tasks starting at logon...")
        break
CloseKey(aKey)
