import wiringpi2 as wpi
import time
import redis

rs = redis.StrictRedis(host='localhost', port=6379, db=0)

wpi.wiringPiSetup()
wpi.mcp3004Setup(70,0)
value = wpi.analogRead(70)


rawcurrent = [0,0,0,0,0,0,0,0,0,0]
rawvoltage = [0,0,0,0,0,0,0,0,0,0]


i=0
while True:
	rawcurrent[i] = (wpi.analogRead(70) *3.3)/1024.0
	rawvoltage[i] = (wpi.analogRead(73) *3.3)/1024.0
	i = (i+1)%10
	sumcurrent =0
	sumvoltage =0
	for j in range(10):
		sumcurrent += rawcurrent[j]
		sumvoltage += rawvoltage[j]
	voltage = sumvoltage
	current = sumcurrent
	power =  int(voltage * current)
	r = rs.set('voltage', sumvoltage)
	r = rs.set('current', sumcurrent)
	r = rs.set('power', sumcurrent)
	time.sleep(.5)
