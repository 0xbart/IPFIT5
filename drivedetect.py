import psutil

__author__ = 'Michael'

print ("The following drives have been detected:")


def driveinfolinux():
    # Cross platform schijf info
    diskinfo = str(psutil.disk_partitions())
    diskinfolist = diskinfo.split('),')
    x = 0
# Split voor aantal aanwezige schijven

    for num in diskinfolist:
        x = x+1
        print ("Drive", x, ":" + num)

# Call function
driveinfolinux()
