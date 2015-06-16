import subprocess
import os

operationSoftware = None

# Determine operating system


def determine():
    global operationSoftware
    if os.name == 'nt':
        print "Windows detected!"
        operationSoftware = "Windows"  # Windows
    elif os.name == 'posix':
        print "Unix detected!"
        operationSoftware = "Unix"  # Mac

# Set up network command


def network():
    global operationSoftware
    if operationSoftware == "Windows":
        with open('networking.txt', "w") as outfile:
            subprocess.call('ipconfig.exe /all', stdout=outfile)
    elif operationSoftware == "Unix":
        with open('networking.txt', "w") as outfile:
            subprocess.call("ifconfig", stdout=outfile)


def sortingProc():
    global operationSoftware
    unixKeywords = ["inet"]
    windowsKeywords = ["IP", "DHCP"]
    temp = []

    if operationSoftware == "Windows":
        print("Windows sorting")
        with open("networking.txt", "r") as file_to_read:
            for line in file_to_read:
                for i, j in enumerate(windowsKeywords):
                    if j in line:
                        temp.append(line + ",")
                    with open("output.txt", "w") as op:
                        op.writelines((items) for items in temp)
    elif operationSoftware == "Unix":
        with open("networking.txt", "r") as file_to_read:
            for line in file_to_read:
                for i, j in enumerate(unixKeywords):
                    if j in line:
                        temp.append(line)
                    with open("output.txt", "w") as op:
                        op.writelines((items) + "," for items in temp)
            print("Output file has been created, check output.txt")


def main():
    determine()
    network()
    sortingProc()

main()
