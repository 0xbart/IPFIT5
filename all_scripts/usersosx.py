import os

__author__ = 'Michael'

try:
    os.popen("dscl . list /Users | grep -v '^_'")
except:
    os.popen("dscacheutil -q user | grep -A 3 -B 2 -e uid:\ 5'[0-9][0-9]'")
