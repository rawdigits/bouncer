#!/usr/bin/python

import shared
import socket
import time

blah = shared.SecondBucketCounter(60)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5555))
s.sendall("C")

def command(data):
  s.sendall(data + "\n")

def processData(data):
    if data['type'] == "connect":
      blah.addItem(data['host'])
      pass

agg = shared.AggregatorConnector()

while True:
  for d in agg.json_read():
    processData(d)
