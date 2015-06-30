import os

__author__ = 'Michaël'

try:
    os.system("dscl . list /Users | grep -v '^_'")
except:
    os.system("dscacheutil -q user | grep -A 3 -B 2 -e uid:\ 5'[0-9][0-9]'")
