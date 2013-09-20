#!/usr/bin/python

import json
import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def process_data(data):
  #print data
  if data['type'] == 'request':
    if data['url'].find('?') > -1:
      url, params = data['url'].split('?')
    else:
       url, params = data['url'], ''
    r.incr("%s" % (data['host']))
    r.expire("%s" % (data['host']), 2)
    r.sadd("uuid", "%s" % (data['uuid']))
  if data['type'] == 'end':
    r.srem("uuid", "%s" % (data['uuid']))
    #r.delete("%s" % (data['uuid']))


agg = shared.AggregatorConnector()
count = 0
while True:
  for d in agg.json_read():
    count += 1
    process_data(d)
    print count
