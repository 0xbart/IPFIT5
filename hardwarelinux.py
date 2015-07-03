import os
import platform

# List hardware on Linux using a command
try:
	print "OS:",  platform.uname()[0]
	print "Distro:", platform.linux_distribution()
	print "Architecture:", platform.architecture()
	print "Processors:" 
	print os.system("grep 'model name' /proc/cpuinfo")
	print "RAM: "
	print os.system("cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'")

except:
	print ("Could not detect hardware")