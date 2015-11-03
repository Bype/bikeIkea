import time
import zmq
import random
import pprint

context = zmq.Context()
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.bind("tcp://127.0.0.1:5557")

result = [0,0,0,0,0,0,0,0]    
c = 0

while True:
    data = consumer_receiver.recv_json()
    result[data['id']] = data['num']
    s = 0
    for n in result:
    	s += n
    if c == 0:
    	print "power :",s
    c = (c + 1) % 20

consumer()
