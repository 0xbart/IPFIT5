import getpass
import socket
import wmi
import math
import platform
from psutil import virtual_memory

def userinfo():
    #Get RAM and CPU name
    try:
        mem = virtual_memory()
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cputype = i.Name

        print("PC name:                            ",  socket.gethostname())
        print("Username:                           ",  getpass.getuser())
        print("System architecture:                ",  platform.machine())
        print("Operating system:                   ",  platform.platform(aliased=0, terse=0))
        print("Processor name:                     ",  cputype)
        print("Processor family:                   ",  platform.processor())
        print("Total virtual memory in Gb:         ", (mem.total/(math.pow(2,30))))
        print("Used virtual memory in Gb           ", (mem.used/(math.pow(2,30))))
        print("Available virtual memory in Gb:     ", (mem.available/(math.pow(2,30))))

    except:
        print "Failure to detect system hardware"

userinfo()