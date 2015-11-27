#!/bin/sh

for i in `/usr/sbin/arp | grep wlan0 | awk '{ print $1 }'`; do 
	ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@$i git -C /home/pi/bikeIkea pull; 
	ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@$i sudo shutdown -r +1
done
