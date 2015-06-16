import subprocess
import os

operationSoftware = None

#Determine operating system
def determine():
    global operationSoftware
    if os.name == 'nt':
        print "Windows detected!"
        operationSoftware = "Windows" #Windows
    elif os.name == 'posix':
        print "Unix detected!"
        operationSoftware = "Unix" #Mac

#Defining network commando's different operation systems
def network():
    global operationSoftware
    if operationSoftware == "Windows":
        with open('unsortedNetworkDetails.txt', "w") as outfile:
            subprocess.call('ipconfig.exe /all', stdout=outfile)
    elif operationSoftware == "Unix":
        with open('unsortedNetworkDetails.txt', "w") as outfile:
            subprocess.call("ifconfig", stdout=outfile)


def sortingProc():
    global operationSoftware
    unixKeywords = ["inet"] #Keywords waarbij binnen Linux gefilterd wordt
    windowsKeywords = ["IP", "DHCP"] #Keywords waar binnen Windows gefilterd wordt
    temp = []

    if operationSoftware == "Windows":
        print("Windows sorting")
        with open("unsortedNetworkDetails.txt", "r") as file_to_read:
            for line in file_to_read:
                if str(windowsKeywords) in line:
                    temp.append(line + ",")
                    with open("output.txt", "w") as op:
                        op.writelines((items) for items in temp)
            print("Output file has been created, check output.txt")
    elif operationSoftware == "Unix":
        with open("unsortedNetworkDetails.txt", "r") as file_to_read:
            for line in file_to_read:
                if str(unixKeywords) in line:
                    temp.append(line)
                    with open("output.txt", "w") as op:
                        op.writelines((items) + "," for items in temp)
            print("Output file has been created, check output.txt")

def main():
    determine()
    network()
    sortingProc()

main()
