import platform

try:
	print 'uname:', platform.uname()

	print 'system   :', platform.system()
	print 'node     :', platform.node()
	print 'release  :', platform.release()
	print 'version  :', platform.version()
	print 'machine  :', platform.machine()
	print 'processor:', platform.processor()
except:
	print "An error occurred"