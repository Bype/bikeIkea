import time
import random
import sys
import pygame
import socket
import liblo
import simplejson
from gelfclient import UdpClient
import redis
rs = redis.StrictRedis(host='localhost', port=6379, db=0)

class Publisher:
	def __init__(self):
		self.zone = rs.get("zone")
		self.bike = rs.get("bike")
		self.myip="myip"
		print(self.zone,self.bike)
		try:	
			self.target = liblo.Address("192.168.100.100",1234)
		except liblo.AddressError as err:
			print(err)
			sys.exit()
		try:
			self.gelf = UdpClient('162.219.4.234', port=12201, mtu=8000, source=socket.gethostname())
		except socket.error, (value,message): 
			print "Could not open socket: " + message 

	def logPower(self,aPower):
		try:
			if self.myip == "myip":
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s.connect(("192.168.100.100",1234))
				self.myip = s.getsockname()[0]
				s.close()

			self.gelf.log("bike"+str(self.bike)+"zone"+str(self.zone),power=aPower,myip=self.myip)
		
		except socket.error, (value,message): 
			print "Could not send log : " + message 

	def pushPower(self,aPower):
		try:
			liblo.send(self.target, "/power",int(self.bike),int(aPower))
		except IOError, message:
			print "Could not send osc message : " +str(message) 


class UIBike:
	def __init__(self):
		self.power = 0
		self.targety = 0
		self.icon = []
		self.currentIcon = 0
		self.nextIcon = 0
		self.iconx = 480
		self.powerRanger =[30,60,90,120,150,200]
		self.lastIcon = time.time()

	def setupScreen(self):
		size = width, height = 480,272
		self.screen = pygame.display.set_mode(size)
		pygame.mouse.set_visible(False)
		self.bg = pygame.image.load("img/bg.jpg").convert()
		self.bgrect = self.bg.get_rect()
		self.scale = pygame.image.load("img/scale.png").convert_alpha()
		self.scalerect = self.scale.get_rect()
		self.shitfy = 265
		self.ratio = (self.scalerect.h-self.shitfy) / 208.0
		self.cropy = self.scalerect.h-self.shitfy
		for i in xrange(6):
			self.icon.append(pygame.image.load("img/%d.png"%(i+1)).convert_alpha())
		self.screen.blit(self.bg,self.bgrect)
		pygame.display.flip()

		
	def setPower(self,p):
		self.power = p
		self.targety = int((self.scalerect.h-self.shitfy)-(self.power*self.ratio))
		if (10<p):
			for ipr in range(0,6):	
				if p < self.powerRanger[ipr]:
					self.setIcon(ipr)
					break
		else:
			self.setIcon(-1)


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
				self.screen.blit(self.icon[self.currentIcon],(self.iconx,44),self.icon[self.currentIcon].get_rect())
				self.iconx += (500-self.iconx)/5
			else:
				self.currentIcon = self.nextIcon
			pygame.display.update((231,0,480,272))
		else:
			if (self.currentIcon!=-1) and(231 < self.iconx):
				self.screen.blit(self.icon[self.nextIcon],(self.iconx,44),self.icon[self.currentIcon].get_rect())
				self.iconx -= (self.iconx-231)/5
			pygame.display.update((231,0,480,272))
		
myBike = UIBike()
myLog = Publisher()

pygame.time.set_timer(pygame.USEREVENT+1, 60000)
pygame.time.set_timer(pygame.USEREVENT+2, 2000)
pygame.time.set_timer(pygame.USEREVENT+3, 300)
myBike.setupScreen()

clock = pygame.time.Clock()
power = 3
while True:
	for event in pygame.event.get():
		if event.type == pygame.USEREVENT+1:
			myLog.logPower(myBike.power)
		if event.type == pygame.USEREVENT+2:
			myLog.pushPower(myBike.power)			            
		if event.type == pygame.QUIT:
			break
		if event.type == pygame.USEREVENT+3:
			myBike.setPower(int(float(rs.get("power"))))
	myBike.update()
	clock.tick(25)
