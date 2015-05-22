# -----------META------------#
#   Hogeschool Leiden
#   Contributors
#   Versions
#   etc

# Import packages
import datetime
import time
import sys
import filehash

# Welcome message
print("Welcome to Pyrensic 0.1 ")

# Timestamp
time = time.time()
timestamp = datetime.datetime.fromtimestamp(time).strftime('%d-%m-%Y %H:%M:%S')
# Investigators name
name = input("Name: ")
# Case number
casenumber = input("Case number: ")
# Organisation
org = input("Organization: ")

# Saving output to a text file
logfile = open("logfile.txt", "w")
logfile.write("Program executed on: " + timestamp + "\n\n" + "By: " + name + "\n" + "Casenumber: " + casenumber + "\n" + "Organization: " + org + "\n")

# "Interface"
print("\n" + "Make a choice: " + "\n"  + "1: File hashing\n" + "2: Data recovery\n" + "3: Example" + "\n" + "0: Exit program" + "\n")

# Input option
options = int(input("Input: " + "\n"))

# Menu config
def menu():
    if options == 1:
        filehash.hash()
    elif options == 2:
        print("Chosen option 2")
    elif options == 3:
        print("Chosen option 3!")
    elif options == 0:
        print("Till next time!")
        sys.exit()
    else:
        print("Not available, make a different choice!")

# Menu is being called.
menu()

# with open("logfile.txt", "a") as logfile:
#   logfile.write("appended text")

if __name__ == '__main__':
    for x in range(100):
        print("\n" + "Choose a function." + "\n"  + "1: File hashing\n" + "2: Data recovery\n" + "3: Example" + "\n" + "0: Exit program" + "\n")
        options = int(input("\n" + "Input:  " + "\n"))
        menu()