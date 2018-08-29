#!/usr/bin/env python2


import sys

zone = sys.argv[1]

print "Setting Zone #",zone

source = open('hostname','r')
data= source.read()
changed=data.replace('zone3server','zone'+str(zone)+'server')
source.close()

target = open('hostname','w')
target.write(changed)
target.close()

source = open('hosts','r')
data= source.read()
changed=data.replace('zone3server','zone'+str(zone)+'server')
source.close()

target = open('hosts','w')
target.write(changed)
target.close()

source = open('hostapd/hostapd.conf','r')
data= source.read()
changed=data.replace('zone3ikcop','zone'+str(zone)+'ikcop')
source.close()

target = open('hostapd/hostapd.conf','w')
target.write(changed)
target.close()
