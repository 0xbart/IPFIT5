__author__ = 'Michael'

import psutil

print ("What do you want to do?")
options = int(input("1: Show drive info" + "\n"))

def driveinfolinux():
#Cross platform schijf info
    diskspartities = str(psutil.disk_partitions())
    diskssplit = diskspartities.split('),')

    for num in diskssplit:
        print (num)

if options == 1:
    driveinfolinux()


