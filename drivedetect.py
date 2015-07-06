import psutil

print ("The following drives have been detected:")


def driveinfolinux():
        try:
            # Cross platform schijf info
            diskinfo = str(psutil.disk_partitions())
            diskinfolist = diskinfo.split('),')
            x = 0
        # Split voor aantal aanwezige schijven
            for num in diskinfolist:
                x = x+1
                print ("Drive", x, ":" + num)
        except:
            print "An error occurred"
# Call function
driveinfolinux()
