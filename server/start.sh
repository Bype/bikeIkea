#!/bin/sh

IP=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
HOSTNAME=`cat /etc/hostname`
MSG=\{\"short_message\":\"startup\",\"host\":\"$HOSTNAME\",\"address\":\"$IP\"\}
echo $MSG
curl -XPOST http://gelf.bype.org/gelf -p0 -d $MSG

python2 consumer.py
