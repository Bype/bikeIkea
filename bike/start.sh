#!/bin/sh

sudo python2 local.py
sudo python2 analogReading.py &
python2 producer.py
