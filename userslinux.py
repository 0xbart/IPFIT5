import os

__author__ = 'Michaël'

try:
    os.system("awk -F':' '{ print $1}' /etc/passwd)")
except:
    os.system("cat /etc/passwd")