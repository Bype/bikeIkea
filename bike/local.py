import wiringpi2 as wiringpi
import simplejson
from subprocess import call

pin_base = 65      # lowest available starting number is 65  
i2c_addr = 0x21

wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c_addr)  

byte = 0
for i in range(0,8):
	wiringpi.pinMode(73+i, 0)
	wiringpi.pullUpDnControl(73+i, 2)
	byte |= ((wiringpi.digitalRead(73+i))<<i)

raw = 255^byte
zone = raw >> 3
bike = raw & 7

config = {
	"zone":zone,
	"bike":bike
}

f = open('/tmp/ikcop.conf', 'w')
simplejson.dump(config, f) 
f.close()

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


