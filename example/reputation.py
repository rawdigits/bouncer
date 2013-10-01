#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
b = shared.BatchCounter(5,20000)

host_requests_per_second = {}
requests_per_second = {}
host_and_url_requests_per_second = {}
user_agents_per_second = {}

def process_data(data):
  global requests_per_second
  #print data
  if data['type'] == 'request':
    time = data['time']/1000
    try:
      user_agents_per_second["%s-%s" % (time, data['headers']['user-agent'])] += 1
    except:
      user_agents_per_second["%s-%s" % (time, data['headers']['user-agent'])] = 1
    try:
      host_requests_per_second["%s-%s" % (time, data['host'])] += 1
    except:
      host_requests_per_second["%s-%s" % (time, data['host'])] = 1
    try:
      requests_per_second[time] += 1
    except:
      requests_per_second[time] = 1
    if b.check():
      for k,v in requests_per_second.items():
        r.incrby(k, v)
      for timehost,count in host_requests_per_second.items():
        time, host = timehost.split('-')
        r.zincrby(time+"-hosts", host, count)
      for timeuseragent,count in user_agents_per_second.items():
        time, useragent = timeuseragent.split('-')
        r.zincrby(time+"-useragents", useragent, count)
      #print host_requests_per_second
      host_requests_per_second.clear()
      requests_per_second.clear()

  if data['type'] == 'end':
    #host_requests_per_second.remove("%s" % (data['uuid']))
    #r.srem("uuid", "%s" % (data['uuid']))
    #print data["uuid"]
    #r.delete("%s" % (data['uuid']))
    pass


agg = shared.AggregatorConnector()
while True:
  for d in agg.json_read():
    process_data(d)
