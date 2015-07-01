import os

# List hardware on OSx using shell command

try:
	scan.write(os.system("system_profiler | grep -A 14 'Hardware overview'")
except:
	print "could not perform hardware scan on this system"