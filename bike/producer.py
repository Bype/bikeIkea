import time
import random
import sys
import pygame
from gelfclient import UdpClient
import socket
import liblo

class Publisher:
	def __init__(self):
		self.bike = random.randrange(0,8)
		self.gelf = UdpClient('162.219.4.234', port=12201, mtu=8000, source=socket.gethostname())
		try:	
			self.target = liblo.Address("localhost",1234)
		except liblo.AddressError as err:
		    print(err)
		    sys.exit()


	def logPower(self,aPower):
		self.gelf.log("bike",power=aPower)

	def pushPower(self,aPower):
		liblo.send(self.target, "/power",self.bike ,aPower)

class UIBike:
	def __init__(self):
		self.power = 0
		self.targety = 0
		self.icon = []
		self.currentIcon = 0
		self.nextIcon = 0
		self.iconx = 480
		self.powerRanger =[10,20,40,80,120,180]
		self.lastIcon = time.time()

	def setupScreen(self):
		size = width, height = 480,272
		self.screen = pygame.display.set_mode(size)
		pygame.mouse.set_visible(False)
		self.bg = pygame.image.load("img/bg.jpg").convert()
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
		for ipr in range(0,6):	
			if p < self.powerRanger[ipr]:
				self.setIcon(ipr)
				break


	def setIcon(self,i):
		if (i != self.nextIcon ) and (i != self.currentIcon) and ( 2 < time.time() - self.lastIcon ) :
			self.nextIcon = i
			self.lastIcon = time.time() 



	def update(self):
		self.screen.blit(self.bg,self.bgrect)
		if self.cropy < self.targety:
			self.cropy += (self.targety-self.cropy)/10
		if self.targety < self.cropy:
			self.cropy -= (self.cropy-self.targety)/10
		self.screen.blit(self.scale,(64,0),(0,self.cropy,self.scalerect.w,self.cropy+272))
		pygame.display.update((64,0,self.scalerect.w,272))
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

pygame.time.set_timer(pygame.USEREVENT+1, 60000)
pygame.time.set_timer(pygame.USEREVENT+2, 1000)
pygame.time.set_timer(pygame.USEREVENT+3, 100)
myBike.setupScreen()

clock = pygame.time.Clock()
power = 3

while True:
	for event in pygame.event.get():
		if event.type == pygame.USEREVENT+1:
			myLog.logPower(myBike.power)
		if event.type == pygame.USEREVENT+2:
			myLog.pushPower(myBike.power)			            
		if event.type == pygame.USEREVENT+3:
			if(power < 199) and (3<=power):
				power += random.randrange(-1,3)
			else:
				power = 3
			myBike.setPower(power)
			if (random.randrange(0,100)<5):
				power = 3
		if event.type == pygame.QUIT:
			break
	myBike.update()
	clock.tick(25)