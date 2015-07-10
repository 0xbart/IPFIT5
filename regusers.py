from _winreg import *

# Make list for folder paths

keylist = []

# Loop through registry for all folders containing user profiles


def userlisting():
    ProfileList = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    regcontent = OpenKey(ProfileList, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList")

# Scan for up to a maximum of 256 folders

    for i in range(256):
        try:
            keyname = EnumKey(regcontent, i)
            keylist.append("r" + "\"" "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
                           + "\\" + str(keyname) + "\"")
        except WindowsError:
            pass
userlisting()

print ("*** Reading from SOFTWARE\Microsoft\WindowsNT\CurrentVersion\ProfileList ***")
folderkeys = keylist

for i in folderkeys:
    print i

kiesregister = str(input("Copy and paste of the specified paths completely, to read profile data:" + "\n"))

aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

for i in folderkeys:
    print '\n\n'
    print '###'
    u = i.replace('r"', '')
    j = u.replace('"', '')
    print 'i: ' + j
    t = OpenKey(aReg, kiesregister)

# list all values for a key
try:
    count = 0
    name, value, type = EnumValue(t, count)
    print (value),
except WindowsError:
    pass
