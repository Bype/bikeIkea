from time import time, sleep
import random
import pprint
import socket
import re
from gelfclient import UdpClient
from liblo import *
import serial
import requests

class DMX:
	def __init__(self):
		self.DMXOPEN=chr(126)
		self.DMXCLOSE=chr(231)
		self.DMXINTENSITY=chr(6)+chr(1)+chr(2)
		self.DMXINIT1= chr(03)+chr(02)+chr(0)+chr(0)+chr(0)
		self.DMXINIT2= chr(10)+chr(02)+chr(0)+chr(0)+chr(0)
		self.ser = serial.Serial('/dev/ttyUSB0')
		self.ser.write( self.DMXOPEN+self.DMXINIT1+self.DMXCLOSE)
		self.ser.write( self.DMXOPEN+self.DMXINIT2+self.DMXCLOSE)
		self.dmxdata=[chr(0)]*513
		self.dmxdata[2]=chr(100)
		self.dmxdata[3]=chr(100)
		self.step = [3,16,30,44,58,72,86,100]
		self.code = [1,5,9,13,17,21,25,29]


	def senddmx(self, chan, intensity):
		# because the spacer bit is [0], the channel number is the array item number
		# set the channel number to the proper value
		self.dmxdata[chan]=chr(intensity)
		# join turns the array data into a string we can send down the DMX
		sdata=''.join(self.dmxdata)
		# write the data to the serial port, this sends the data to your fixture
		self.ser.write(self.DMXOPEN+self.DMXINTENSITY+sdata+self.DMXCLOSE)
        
	def sendPercent(self,percent):
		for i in range(8):
			if percent < self.step[i]:
				self.senddmx(1,self.code[i])
				break


class Consumer(ServerThread):
	def __init__(self):
		try:
			self.gelf = UdpClient('162.219.4.234', port=12201, mtu=8000, source=socket.gethostname())
		except socket.error, (value,message): 
			print "Could not open socket: " + message 
		self.result = [0,0,0,0,0,0,0,0]    
		ServerThread.__init__(self, 1234)
		self.sum = 0
		self.zone = re.match(r'(.*)server',socket.gethostname()).group(1)
		self.zonen = re.match(r'zone(.*)',self.zone).group(1)
		self.dmx = DMX()


	@make_method('/power','ii')
	def foo_callback(self, path, args):
		bike,power = args
		self.result[bike] = int(power)
		self.sum=0
		for n in self.result:
			self.sum += n	

	def updateDMX(self):
		self.dmx.sendPercent((100*self.sum)/600)

	def publish(self):
		try:
			requests.get('http://ikcop.bype.org/set/ccf82dd-807d-4f63-a30b-c78e53072a38/zone/'+self.zonen+'/'+str(self.sum))
		except requests.exceptions.RequestException as e:
			print e

		try:
			self.gelf.log(self.zone,sum=self.sum,details=self.result.__str__())
		except socket.error, (value,message): 
			print "Could not open socket: " + message 

try:
    server = Consumer()
except ServerError as err:
    print(err)
    sys.exit()

server.start()

c = 0
while True:
	if c==0:
		server.publish()
	c = (c+1)%60
	server.updateDMX()
	sleep(1)

