import os

__author__ = 'Michael'

try:
    os.system("awk -F':' '{ print $1}' /etc/passwd)")
except:
    os.system("cat /etc/passwd")