from sys import platform as _platform
import subprocess

def detect_os():
    if _platform == 'linux' or _platform == 'linux2':
        subprocess.call(['initctl show-config'], shell=True)
    else:
        print("This script is for Linux only.")


detect_os()