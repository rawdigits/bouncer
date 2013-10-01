#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
b = shared.BatchCounter(5,20000)

metric = {}

def process_data(data):
  global metric
  #print data
  if data['type'] == 'request':
    time = data['time']/1000
    TIME_LENGTH=10

    try:
      metric["%s-%s" % (time, data['headers']['user-agent'])] += 1
    except KeyError:
      try:
        metric["%s-%s" % (time, data['headers']['user-agent'])] = 1
      except:
        pass

    if b.check():
      #using slices in these because it seems faster..
      for k,v in metric.items():
        time, url = k[0:10], k[11:]
        r.zincrby(time+"-urls", url, v)

      metric.clear()


agg = shared.AggregatorConnector()

while True:
  for d in agg.json_read():
    process_data(d)