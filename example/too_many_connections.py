#!/usr/bin/python

import shared
import socket
import time

blah = shared.SecondBucketCounter(5)

def processData(data):
  if data['type'] == "connect":
    host = data['host']
    blah.addItem(host)
    if blah.checkItem(host, 75):
      agg.write("BLOCK %s|10000" % host)

agg = shared.AggregatorConnector()

while True:
  for d in agg.json_read():
    processData(d)
