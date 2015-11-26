#!/bin/sh

for i in `arp | grep wlan0 | awk '{ print $1 }'`; do 
	ssh pi@$i git -C /home/pi/bikeIkea pull; 
done
