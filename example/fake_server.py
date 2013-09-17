#!/usr/bin/python

import json
import socket
import time

data = {"host":"10.0.10.163","url":"/test.html","method":"GET","headers":{"user-agent":"httperf/0.9.0","host":"10.0.10.163","x-forwarded-for":"10.0.10.163","x-forwarded-port":60329,"x-forwarded-proto":"http"},"uuid":"04670e16-6ae9-4421-b42b-1cf211e2d046"}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5555))
s.sendall("S")


while True:
#  try:
  s.send(json.dumps(data)+"\n")

#  if data.count("\n") > 1:
#    print "FOUND"
#    data = data.split("\n")[0]
#  print data
#  print '---'
#  j = json.loads(data)
#  except:
#    print "Incomplete %s" % j
#  try:
#    url, params = j['url'].split('?')
#  except:
#    url, params = j['url'], None
#  #print "%s %s\n    %s" % (j['method'], url, params)
