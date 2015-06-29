import os
import psutil

"""
Script:         Cloud.py
Creator:        Wesley Boumans
Dependencies:   pip install psutil; 
Platform:       Windows
"""

print("Checking file system for traces of cloud usage..\n")
print("Application:         Status:")

if os.path.isdir("C:\\Program Files (x86)\\Google\\Drive"):
    print("Google Drive         detected")
    google_drive = []
    for p in psutil.process_iter():
        try:
            if p.name() == 'googledrivesync.exe':
                google_drive.append(p)
                print("Google Drive         running PID" + str(p))
        except psutil.Error:
            pass
else:
    print("Google Drive         not found")

if os.path.isdir("C:\\Program Files (x86)\\Dropbox"):
    print("\nDropbox              detected")
    dropbox = []
    for p in psutil.process_iter():
        try:
            if p.name() == 'Dropbox.exe':
                dropbox.append(p)
                print("Dropbox              running PID" + str(p))
        except psutil.Error:
            pass
else:
    print("Dropbox              not found")

if os.path.isdir("C:\\Program Files (x86)\\Microsoft OneDrive"):
    print("\nOneDrive             detected")
    one_drive = []
    for p in psutil.process_iter():
        try:
            if p.name() == 'OneDrive.exe':
                one_drive.append(p)
                print("OneDrive             running PID" + str(p))
        except psutil.Error:
            pass
else:
    print("OneDrive             not found")

if os.path.isdir("C:\\Program Files (x86)\\Evernote"):
    print("\nEvernote             detected")
    evernote = []
    for p in psutil.process_iter():
        try:
            if p.name() == 'Evernote.exe':
                evernote.append(p)
                print("Evernote             running PID" + str(p))
        except psutil.Error:
            pass
else:
    print("Evernote             not found")

