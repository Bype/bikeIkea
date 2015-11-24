from subprocess import call

for n in range(1,33):
	print n
	call(["ssh", "pi@192.168.100."+str(n),"sudo shutdown +1"])


