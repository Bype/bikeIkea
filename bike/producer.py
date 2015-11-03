import time
import zmq
import random
import sys
import pygame

def producer():
	context = zmq.Context()
	zmq_socket = context.socket(zmq.PUSH)
	prod_id = int(sys.argv[1])
	print "I am consumer #%s" % (prod_id)
	zmq_socket.connect("tcp://127.0.0.1:5557")
    # Start your result manager and workers before you start your producers
	for num in xrange(20000):
		work_message = { 'id':prod_id,'num' :  random.randrange(0,250)}
		zmq_socket.send_json(work_message)
		time.sleep(random.randrange(20,200)/100.0)

#producer()


class UIBike:
	def __init__(self):
		self.power = 0
		self.targety = 0
		self.icon = []

	def setupScreen(self):
		size = width, height = 480,272
		self.screen = pygame.display.set_mode(size)
		pygame.mouse.set_visible(False)
		self.bg = pygame.image.load("img/bg.png").convert()
		self.bgrect = self.bg.get_rect()
		self.scale = pygame.image.load("img/scale.png").convert_alpha()
		self.scalerect = self.scale.get_rect()
		self.ratio = (self.scalerect.h-272) / 200.0
		self.cropy = self.scalerect.h-272
		for i in xrange(6):
			self.icon.append(pygame.image.load("img/%d.png"%(i+1)).convert_alpha())
		self.screen.blit(self.bg,self.bgrect)
		pygame.display.update()


		
	def setPower(self,p):
		self.power = p
		self.targety = int((self.scalerect.h-272)-(self.power*self.ratio))

	def update(self):
		self.screen.blit(self.bg,self.bgrect)
		if self.cropy < self.targety:
			self.cropy += (self.targety-self.cropy)/10
		if self.targety < self.cropy:
			self.cropy -= (self.cropy-self.targety)/10
		self.screen.blit(self.scale,(64,0),(0,self.cropy,self.scalerect.w,self.cropy+272))
		pygame.display.update((64,0,147,272))


myBike = UIBike()

myBike.setupScreen()

c = 0

while myBike.power < 200:
	myBike.update()
	time.sleep(0.04)
	if c%100==0:
		myBike.setPower(random.randrange(0,200));
	c = (c+1)%100

while True:
	myBike.update()