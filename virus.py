import json
import hashlib
import os
import os.path
import time
import re
import requests
from virus_total_apis import PublicApi as VirusTotalPublicApi
# pip install virustotal-api
requests.packages.urllib3.disable_warnings()

stepCount = 0  # Variable to count the files left
hashList = []  # The hash list for VirusTotal
fullList = []  # The full list with filenames to link hashes to files

virusLogfile = ("./VirusTotal.txt")
hashLogFile = ("./filesWithHashValues.txt")

if os.path.isfile(virusLogfile):  # Check if the text files already exists
    os.remove("VirusTotal.txt")  # Text files get deleted upon detection
elif os.path.isfile(hashLogFile):
    os.remove("filesWithHashValues.txt")

print("Use absolute paths to specify the folder! i.e. C:\Users")

try: # User inputs the file path he would like to check
    filepath = raw_input("Which folder would you like to" +
    "check for malicious software? ")
except IOError:
    print("Try again")


def filehash(filepath):  # Function to hash the working directory
    blocksize = 64*1024
    md5 = hashlib.md5()
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

for root, dirs, files in os.walk(filepath): # Walks the directory and appends them to lists
    for fpath in [os.path.join(root, f) for f in files]:
        md5 = filehash(fpath)
        hashList.append(md5)
        fullList.append(md5)
        name = os.path.relpath(fpath, filepath)
        fullList.append(name)
        with open("filesWithHashValues.txt", "a") as myfile:
           myfile.write('%s, %s, %s' % (md5, name, '\n'))


def displayInfo():  # Displays some information about the estimated time needed
        global stepCount
        timeToGo = (int(len(hashList)) - stepCount) * 15 / 60
        itemsLeft = (int(len(hashList)) - stepCount)
        print("\nThere are " + str(itemsLeft) + " item(s) left to be verified.")
        print("Time for completion: " + str(timeToGo) + " minutes")


def virusTotal():  # Function that gets the actual results from VirusTotal.com
    global stepCount
    for i, item in enumerate(hashList):
        stepCount = stepCount + 1
        API_KEY = 'c5fe9c9e314948e0ede7a412bb2265a54596a4a3c61abf03e7af07c4f12237b5'
        vt = VirusTotalPublicApi(API_KEY)
        response =  vt.get_file_report(item)
        with open("VirusTotal.txt", "a") as textfile:
            textfile.write(json.dumps(response, textfile, sort_keys=False, indent=4))
        displayInfo()
        time.sleep(15)


def checkResults(): # Checks the output files for any infected files
    try:
        b = open("VirusTotal.txt")
        positiveCounter = 0
        for line in b:
            if re.match("(.*)(positives)(.*)[1-99]", line):
                positiveCounter = positiveCounter + 1
        if positiveCounter >= 1:
            print("There are " + str(positiveCounter) + " file(s) infected.")
        else:
            print("You are free of any known malicious software")
    except IOError:
        print("\nThe folder " + filepath + " does not exists..")
        print("Try again")


def main():  # Calls all the functions at a specific order
    displayInfo()
    virusTotal()
    checkResults()

main()
