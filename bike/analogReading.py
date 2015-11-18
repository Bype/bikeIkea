import wiringpi2 as wpi
import time
import redis
import math

rs = redis.StrictRedis(host='localhost', port=6379, db=0)

wpi.wiringPiSetup()
wpi.mcp3004Setup(70,0)

rawvoltage = [0,0,0,0,0,0,0,0,0,0]

i=0
while True:
	rawvoltage[i] = (wpi.analogRead(73) *33)/1024.0
	i = (i+1)%10
	sumvoltage =0
	for j in range(10):
		sumvoltage += rawvoltage[j]
	power =  int(math.floor(13 * sumvoltage))
	if 200 < power:
		power = 200
	r = rs.set('voltage', sumvoltage)
	r = rs.set('power', power)
	time.sleep(.1)
