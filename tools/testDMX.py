import liblo
import time

target = liblo.Address("192.168.100.100",1234)
for i in range(65):
	print "sending : ",i

	liblo.send(target, "/power",0,10*i)
	time.sleep(1)

