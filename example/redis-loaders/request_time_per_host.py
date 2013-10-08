#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
b = shared.BatchCounter(5,10000)
agg = shared.AggregatorConnector()

metric  = {}
metric2 = {}
granularity = 60

def process_data(data):
  global metric
  #print data
  if data['type'] == 'request':
    # assign these inside the if because there are tons of connect events..
    request_time = data['time']
    #request_time = ((data['time']/1000)/granularity)*granularity
    uuid = data['uuid']
    TIME_LENGTH=10
    try:
      metric[uuid] = {"time":request_time, "host":data['host']}
    except:
      print "this shouldn't happen"
  elif data['type'] == 'end':
    # assign these inside the if because there are tons of connect events..
    request_time = data['time']
    uuid = data['uuid']
    #print metric
    if metric.has_key(uuid):
      metric2[metric[uuid]["host"]] = request_time - metric[uuid]["time"]
      #print metric2[metric[uuid]["host"]]
      metric.pop(uuid)

  if b.check():
    #using slices in these because it seems faster..
    now = (int(time.time())/granularity)*granularity
    for k,v in metric2.items():
      r.zincrby(str(now)+"-hosttime", k, v)
    metric2.clear()



while True:
  for d in agg.json_read():
    process_data(d)
