#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
hosts = {}
seconds = {}
b = shared.BatchCounter(5,20000)

def process_data(data):
  global total
  global seconds
  #print data
  if data['type'] == 'request':
#    now = int(time.time())
#    if data['url'].find('?') > -1:
#      url, params = data['url'].split('?')
#    else:
#       url, params = data['url'], ''
    #r.incr("%s" % (data['host']))
    #r.incr("%s" % (data['time']/1000))
    #r.expire("%s" % (data['host']), 20)
    #r.sadd("uuid", "%s" % (data['uuid']))
    #print data["uuid"]
    time = data['time']/1000
    total += 1
    try:
      hosts["%s-%s" % (time, data['host'])] += 1
    except:
      hosts["%s-%s" % (time, data['host'])] = 1
    try:
      seconds[data['time']/1000] += 1
    except:
      seconds[data['time']/1000] = 1
    if b.check():
      #for k,v in seconds.items():
      #  r.incrby(k, v)
      #print hosts
      for timehost,count in hosts.items():
        time, host = timehost.split('-')
        r.zincrby(time, host, count)
      print hosts
      hosts.clear()

      seconds = {}
      print seconds
      print total

  if data['type'] == 'end':
    #hosts.remove("%s" % (data['uuid']))
    #r.srem("uuid", "%s" % (data['uuid']))
    #print data["uuid"]
    #r.delete("%s" % (data['uuid']))
    pass


agg = shared.AggregatorConnector()
total = 0
while True:
  for d in agg.json_read():
    process_data(d)
