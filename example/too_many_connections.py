#!/usr/bin/python

import shared
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
    if all_connects.count(item) > 50:
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
    if data['type'] == "connect":
      blah.addItem(data['host'])
      pass

agg = shared.AggregatorConnector()

while True:
  for d in agg.json_read():
    processData(d)
