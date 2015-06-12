__author__ = 'Michael'

import getpass
import socket
import sysinfo
import platform
import psutil

def userinfo():
#User info
    print ("Network name:           ",  socket.gethostname())
    print ("Username:               ",  getpass.getuser())
    print ("System architecture:    ",  platform.machine())
    print ("Operating system        ",  platform.platform(aliased=0, terse=0))
    print ("Processor:              ",  platform.processor())
    print ("Virtual memory:         ",  psutil.virtual_memory())
    print ("Virtual memory:         ",  sysinfo.memory_available())
userinfo()
