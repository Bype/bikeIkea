import time
import zmq
import random
import pprint
import socket
from gelfclient import UdpClient


class Consumer:
	def __init__(self):
		self.gelf = UdpClient('log.bype.org', port=12201, mtu=8000, source=socket.gethostname())
		context = zmq.Context()
		self.zmq = context.socket(zmq.PULL)
		self.zmq.bind("tcp://0.0.0.0:5557")	
		self.result = [0,0,0,0,0,0,0,0]    

	def consume(self):
		data = self.zmq.recv_json()
		self.result[data['bike']] = data['power']
		self.sum=0
		for n in self.result:
			self.sum += n

	def publish(self):
		print self.result," ",self.sum
		self.gelf.log("zone",sum=self.sum,details=self.result.__str__())



myConsumer = Consumer()
c=0

while True:
	myConsumer.consume()
	if c == 0:
		myConsumer.publish()
	c = (c + 1) % 10

