import time
import zmq
import random
import sys
import pygame
from gelfclient import UdpClient
import socket


class Publisher:
	def __init__(self):
		self.gelf = UdpClient('log.bype.org', port=12201, mtu=8000, source=socket.gethostname())
		context = zmq.Context()
		self.zmq = context.socket(zmq.PUSH)
		self.zmq.connect("tcp://127.0.0.1:5557")

	def logPower(self,aPower):
		self.gelf.log("bike",power=aPower)

	def pushPower(self,aPower):
		self.zmq.send_json({ 'bike':1,'power' :  aPower})


class UIBike:
	def __init__(self):
		self.power = 0
		self.targety = 0
		self.icon = []
		self.currentIcon = 0
		self.nextIcon = 0
		self.iconx = 240

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
		pygame.display.flip()

		
	def setPower(self,p):
		self.power = p
		self.targety = int((self.scalerect.h-272)-(self.power*self.ratio))

	def setIcon(self,i):
		self.nextIcon = i


	def update(self):
		self.screen.blit(self.bg,self.bgrect)
		if self.cropy < self.targety:
			self.cropy += (self.targety-self.cropy)/10
		if self.targety < self.cropy:
			self.cropy -= (self.cropy-self.targety)/10
		self.screen.blit(self.scale,(64,0),(0,self.cropy,self.scalerect.w,self.cropy+272))
		pygame.display.update((64,0,147,272))
		if self.currentIcon != self.nextIcon:
			if(self.iconx<480):
				self.screen.blit(self.icon[self.currentIcon],(self.iconx,36),self.icon[self.currentIcon].get_rect())
				self.iconx += (500-self.iconx)/5
			else:
				self.currentIcon = self.nextIcon
			pygame.display.update((240,0,480,272))
		else:
			if(240 < self.iconx):
				self.screen.blit(self.icon[self.nextIcon],(self.iconx,36),self.icon[self.currentIcon].get_rect())
				self.iconx -= (self.iconx-240)/5
			pygame.display.update((240,0,480,272))
		
myBike = UIBike()
myLog = Publisher()

pygame.time.set_timer(pygame.USEREVENT+1, 20000)
pygame.time.set_timer(pygame.USEREVENT+2, 1000)
pygame.time.set_timer(pygame.USEREVENT+3, 10000)
myBike.setupScreen()

clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		if event.type == pygame.USEREVENT+1:
			myLog.logPower(myBike.power)
		if event.type == pygame.USEREVENT+2:
			myLog.pushPower(myBike.power)			            
		if event.type == pygame.USEREVENT+3:
			myBike.setPower(random.randrange(0,200))
			myBike.setIcon(random.randrange(1,5))
		if event.type == pygame.QUIT:
			break
	myBike.update()
	clock.tick(25)