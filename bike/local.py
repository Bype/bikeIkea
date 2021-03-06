import wiringpi2 as wiringpi
import simplejson
from subprocess import call
import redis
rs = redis.StrictRedis(host='localhost', port=6379, db=0)

pin_base = 65      # lowest available starting number is 65  
i2c_addr = 0x20

wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c_addr)  

byte = 0
for i in range(0,8):
	wiringpi.pinMode(65+i, 0)
	wiringpi.pullUpDnControl(65+i, 2)


for i in range(0,8):
	print(i,wiringpi.digitalRead(65+i))
	byte |= ((wiringpi.digitalRead(65+i))<<i)

wiringpi.pinMode(73,1)
wiringpi.pinMode(74,1)
wiringpi.digitalWrite(73,1)
wiringpi.digitalWrite(74,1)


raw = 255^byte
zone = raw >> 3
bike = raw & 7

rs.set("zone",zone)
rs.set("bike",bike)

source = open('./wpa_supplicant.conf','r')
target = open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
data= source.read()
changed=data.replace('zone#ikcop','zone'+str(zone)+'ikcop')
target.write(changed)
source.close()
target.close()

call(["ifdown", "wlan0"])
call(["ifup", "wlan0"])

print "zone%dbike%d" % (zone,bike)


