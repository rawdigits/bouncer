#!/usr/bin/python

import json
import socket
import time

class AggregatorConnector:

  def __init__(self, aggregator=("127.0.0.1",5555), mode="C"):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect(aggregator)
    self.socket.sendall(mode)
    self.previous_data = ''

  def write(self, data):
    self.socket.sendall(data + "\n")

  def raw_read(self):
    records = []
    new_data = self.socket.recv(8)
    data = self.previous_data + new_data
    if data.count("\n") > 1:
      if data[-1] == '\n':
        for d in data.split("\n")[:-1]:
          records.append(d)
        self.previous_data = ''
      else:
        good = data.split("\n")
        for d in good[:-2]:
          records.append(d)
        self.previous_data = good[:-1]
    elif data.count("\n") == 1:
      if data[-1] == '\n':
        records.append(data)
        self.previous_data = ''
      else:
        good = data.split('\n')
        records.append(good[0])
        self.previous_data = good[1]
      #print "ONE"
    else:
      self.previous_data = data
      #print "EXTRA"
      #print data
    return records

#    if data[-1] == "\n":
#      return [d]
#    #if data[0] == '{' and data[-1] == "\n":
#      if data[-1] == "\n":
#      if data.count("\n") > 1:
#      else:
#        return [data.rstrip('\n')]
#    else:
#      return []

  def json_read(self):
    data = self.raw_read()
    try:
      return [json.loads(line) for line in data]
    except:
      print data
#    if data != []:
    #  try:
#    else:
#      return []
    #  except:
    #    print data
    #    return []



