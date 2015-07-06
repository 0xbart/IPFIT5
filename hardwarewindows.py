import getpass
import socket
import wmi
import math
import platform
from psutil import virtual_memory

__author__ = 'Michael'

# WMI is used to get the processor type and stats

hardwarelist = []


def userinfo():
    try:
        mem = virtual_memory()
        c = wmi.WMI()
        for i in c.Win32_Processor():
            cputype = i.Name

    # List of hardware detection functions
    # math.pow function to convert mem. output to human readable numbers
        hardwarelist = ["PC name:                            " +
                        socket.gethostname(),
                        "Username:                           " +
                        getpass.getuser(),
                        "System architecture:                " +
                        platform.machine(),
                        "Operating system:                   " +
                        platform.platform(aliased=0, terse=0),
                        "Processor name:                     " +
                        cputype,
                        "Processor family:                   " +
                        platform.processor(),
                        "Total virtual memory in Gb:         " +
                        str((mem.total/(math.pow(2, 30)))),
                        "Used virtual memory in Gb           " +
                        str((mem.used/(math.pow(2, 30)))),
                        "Available virtual memory in Gb:     " +
                        str((mem.available/(math.pow(2, 30))))
                        ]

# If ImportError occurs, pass so program doesn't crash
    except ImportError:
        pass

        # Loop through list and print the functions
    try:
        for i in hardwarelist:
            print i
    except:
        pass

userinfo()
