#!/usr/bin/python

import json
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5555))
s.sendall("C")

def command(data):
  s.sendall(data + "\n")

def processData(data):
  if data.strip() != '':
    print data
#    try:
    j = json.loads(data)
#    except:
#      print "Bad data: %s" % data
    if j['url'].find('?') > -1:
      url, params = j['url'].split('?')
    else:
      url, params = j['url'], ''
    if j['url'] == '/test.html':
      command("block %s|10000" % j['host'])
    print "%s %s\n    %s" % (j['method'], url, params)


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
