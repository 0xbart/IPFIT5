# -----------META------------#
#   Hogeschool Leiden
#   Contributors
#   Versions
#   etc

# Import packages
import datetime
import time
import sys

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

print("1: File hashing\n" + "2: Data recovery\n" + "3: Example" + "\n" + "0: Exit program" + "\n")

options = int(input("Choose a option: " + "\n"))

# Menu config
def menu():
    if options == 1:
        print("Chosen option 1!")
    elif options == 2:
        print("Chosen option 2!")
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