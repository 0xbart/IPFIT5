import getpass
import socket
import wmi
import math
import platform
from psutil import virtual_memory

def userinfo():
    try:
        mem = virtual_memory()
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cputype = i.Name

        hardwarelist = ["PC name:                            " + socket.gethostname(),
                        "Username:                           " +  getpass.getuser() ,
                        "System architecture:                " +  platform.machine(),
                        "Operating system:                   " +  platform.platform(aliased=0, terse=0),
                        "Processor name:                     " +  cputype,
                        "Processor family:                   " +  platform.processor(),
                        "Total virtual memory in Gb:         " + str((mem.total/(math.pow(2,30)))),
                        "Used virtual memory in Gb           " + str((mem.used/(math.pow(2,30)))),
                        "Available virtual memory in Gb:     " + str((mem.available/(math.pow(2,30))))
                        ]
    except ImportError:
		pass
        
        #Get RAM and CPU name
    try:
        for i in hardwarelist:
            print i
    except:
        pass

userinfo()

