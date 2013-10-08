#!/usr/bin/python

import shared
import socket
import time

PROTECT_URL = '/slow'

blah = shared.SecondBucketCounter(60)
agg = shared.AggregatorConnector()
agg.write('durl %s' % PROTECT_URL)

def processData(data):
    if data['type'] == "request":
      if data['url'] == PROTECT_URL:
        host = data['host']
        blah.addItem(host)
        if blah.checkItem(host, 2):
          agg.write("grey %s|60000" % host)



while True:
  for d in agg.json_read():
    processData(d)
