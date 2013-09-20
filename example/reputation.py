#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
blah = set()

def process_data(data):
  #print data
  if data['type'] == 'request':
    if data['url'].find('?') > -1:
      url, params = data['url'].split('?')
    else:
       url, params = data['url'], ''
    r.incr("%s" % (data['host']))
    r.expire("%s" % (data['host']), 20)
    r.sadd("uuid", "%s" % (data['uuid']))
    #blah.add("%s" % (data['uuid']))
  if data['type'] == 'end':
    #blah.remove("%s" % (data['uuid']))
    r.srem("uuid", "%s" % (data['uuid']))
    #r.delete("%s" % (data['uuid']))
    pass


agg = shared.AggregatorConnector()
while True:
  for d in agg.json_read():
    process_data(d)
