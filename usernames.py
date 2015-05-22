__author__ = 'Michael'

import getpass
import socket

def userinfo():
#User info
    print ("Hostname:", socket.gethostname())
    print ("Username:", getpass.getuser())

userinfo()
