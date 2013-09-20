#!/usr/bin/python

import json
import socket
import time
import redis

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5555))
s.sendall("C")

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def command(data):
  s.sendall(data + "\n")

def processData(data):
  if data.strip() != '':
#    try:
    j = json.loads(data)
    print j
#    except:
#      print "Bad data: %s" % data
    if j['type'] == 'request':
      if j['url'].find('?') > -1:
        url, params = j['url'].split('?')
      else:
        url, params = j['url'], ''
      if j['url'] == '/test.html':
        command("block %s|10000" % j['host'])
      #r.incr("%s:%s" % (j['host'], url))
      r.incr("%s" % (j['host']))
      r.expire("%s" % (j['host']), 2)
      r.incr("%s" % (j['uuid']))
      #print "%s:%s" % (j['host'], url)
    if j['type'] == 'end':
      r.delete("%s" % (j['uuid']))
      #print j
      #r.decr("%s" % (j['host']))


while True:
#  try:
  data = s.recv(8000)
  if data[0] == '{' and data[-1] == "\n":

    if data.count("\n") > 1:
      #print "FOUND"
      #print data
      #print '---'
      #print len(data.split("\n"))
      for d in data.split("\n"):
        #print 'splitting'
        processData(d)
    else:
      #print 'not split'
      processData(data)
#  else:
#    data += data
