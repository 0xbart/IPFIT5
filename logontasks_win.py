from _winreg import *

__author__ = 'Michaël'

# Read the registry at printed location for logon tasks

print (r"*** Reading from registry"
       "SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
       )

# Connect with the registry and open the specified key

aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")

# Loop through the registry for entries, and count them.
# N = name of entry, V = the value (name of folder and associated .exe files)

for i in range(1024):
    try:
        n, v, t = EnumValue(aKey, i)
        print (i+1, n, v)
    except EnvironmentError:
        print ("You have", i,
               "tasks starting at logon, that are recorded in the registry.")
        break

CloseKey(aKey)
