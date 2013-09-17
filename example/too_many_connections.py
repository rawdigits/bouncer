#!/usr/bin/python

import json
import socket
import time

class SecondBucketCounter:
  def __init__(self, seconds):
    self.buckets = [[]]
    self.seconds = seconds
    self.previous_now = int(time.time())
  def addItem(self, item):
    now = int(time.time())
    if now == self.previous_now:
      self.buckets[-1].append(item)
    elif now > self.previous_now:
      self.buckets.append([])
      self.buckets[-1].append(item)
      if len(self.buckets) > self.seconds:
        self.buckets.pop(0)
    all_connects = [item for sublist in self.buckets for item in sublist]
    self.previous_now = now
    if all_connects.count(item) > 200:
      command("BLOCK %s|10000\n" % item)
    #print len(self.buckets)
    #print len(all_connects)

blah = SecondBucketCounter(60)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5555))
s.sendall("C")

def command(data):
  s.sendall(data + "\n")

def processData(data):
  if data.strip() != '':
    #print data
    j = json.loads(data)
    if j['type'] == "connect":
      blah.addItem(j['host'])
      pass
      #print "%s\n" % (j['host'])


while True:
#  try:
  data = s.recv(8000)
  if data[0] == '{' and data[-1] == "\n":

    if data.count("\n") > 1:
      for d in data.split("\n"):
        #print 'splitting'
        processData(d)
    else:
      #print 'not split'
      processData(data)
