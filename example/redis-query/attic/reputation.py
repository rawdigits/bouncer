#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
b = shared.BatchCounter(5,2000)

host_requests_by_second = {}
requests_by_second = {}
host_and_url_requests_by_second = {}
user_agents_by_second = {}
url_by_second = {}

def process_data(data):
  global requests_by_second
  #print data
  if data['type'] == 'request':
    time = data['time']/1000
    TIME_LENGTH=10

    #leaving this section really waterfall for make speed
    try:
      user_agents_by_second["%s-%s" % (time, data['headers']['user-agent'])] += 1
    except KeyError:
      try:
        user_agents_by_second["%s-%s" % (time, data['headers']['user-agent'])] = 1
      except:
        pass

    try:
      host_and_url_requests_by_second["%s-%s" % (time, data['host']+data['url'])] += 1
    except:
      host_and_url_requests_by_second["%s-%s" % (time, data['host']+data['url'])] = 1

    try:
      host_requests_by_second["%s-%s" % (time, data['host'])] += 1
    except:
      host_requests_by_second["%s-%s" % (time, data['host'])] = 1

    try:
      requests_by_second[time] += 1
    except:
      requests_by_second[time] = 1

    try:
      url_by_second["%s-%s" % (time, data['url'])] += 1
    except:
      url_by_second["%s-%s" % (time, data['url'])] = 1

    if b.check():
      #using slices in these because it seems faster..
      for k,v in requests_by_second.items():
        r.incrby(k, v)
      for k,v in host_and_url_requests_by_second.items():
        time, hosturl = k[0:10], k[11:]
        r.zincrby(time+"-hosturls", hosturl, v)
      for k,v in host_requests_by_second.items():
        time, host = k[0:10], k[11:]
        r.zincrby(time+"-hosts", host, v)
      for k,v in user_agents_by_second.items():
        time, useragent = k[0:10], k[11:]
        r.zincrby(time+"-useragents", useragent, v)
      for k,v in url_by_second.items():
        time, url = k[0:10], k[11:]
        r.zincrby(time+"-urls", url, v)

      #print host_requests_by_second

      host_requests_by_second.clear()
      requests_by_second.clear()
      url_by_second.clear()


  if data['type'] == 'end':
    #host_requests_by_second.remove("%s" % (data['uuid']))
    #r.srem("uuid", "%s" % (data['uuid']))
    #print data["uuid"]
    #r.delete("%s" % (data['uuid']))
    pass


agg = shared.AggregatorConnector()
while True:
  for d in agg.json_read():
    process_data(d)
