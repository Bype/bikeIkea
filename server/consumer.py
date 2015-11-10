from time import time, sleep
import random
import pprint
import socket
from gelfclient import UdpClient
from liblo import *

class Consumer(ServerThread):
	def __init__(self):
		self.gelf = UdpClient('162.219.4.234', port=12201, mtu=8000, source=socket.gethostname())
		self.result = [0,0,0,0,0,0,0,0]    
		ServerThread.__init__(self, 1234)
		self.sum = 0

	@make_method('/power','ii')
	def foo_callback(self, path, args):
		bike,power = args
		self.result[bike] = power
		self.sum=0
		for n in self.result:
			self.sum += n
		print self.sum

	@make_method(None, None)
	def fallback(self, path, args):
		print("received unknown message '%s'" % path)	

	def publish(self):
		print self.result," ",self.sum
		self.gelf.log("zone",sum=self.sum,details=self.result.__str__())


try:
    server = Consumer()
except ServerError as err:
    print(err)
    sys.exit()

server.start()


while True:
	server.publish()
	sleep(10)

