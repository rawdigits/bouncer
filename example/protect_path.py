#!/usr/bin/python

import shared
import socket
import time

PROTECT_URL = '/slow'

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
    all_views = [item for sublist in self.buckets for item in sublist]
    self.previous_now = now
    if all_views.count(item) > 2:
      #command("block %s|1\n" % item)
      print 'sent greylist entry'
      command("grey %s|60000" % item)
    #print len(self.buckets)
    #print len(all_views)

blah = SecondBucketCounter(60)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5555))
s.send("C")
time.sleep(.5)

def command(data):
  s.send(data + "\n")

def processData(data):
    if data['type'] == "request":
      if data['url'] == PROTECT_URL:
        blah.addItem(data['host'])
        pass

agg = shared.AggregatorConnector()

command('durl %s' % PROTECT_URL)

while True:
  for d in agg.json_read():
    processData(d)
