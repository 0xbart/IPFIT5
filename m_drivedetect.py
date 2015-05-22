__author__ = 'Michael'

import psutil

print ("What do you want to do?")
options = int(input("1: Show drive info" + "\n"))

def driveinfolinux():
#Cross platform schijf info
    diskinfo = str(psutil.disk_partitions())
    diskinfolist = diskinfo.split('),')
    x = 0
#Split voor aantal aanwezige schijven
    for num in diskinfolist:
        x = x+1
        print ("Drive",x, ":" + num)

#Call function
if options == 1:
    driveinfolinux()
