import simplejson as json
import socket
import time

class BatchCounter:

  def __init__(self, seconds, ticks):
    self.seconds = seconds
    self.time = int(time.time())
    self.count = 0
    self.ticks = ticks

  def check(self):
    now = int(time.time())
    self.count += 1
    if self.count >= self.ticks:
      self.count = 0
      self.time = now
      return True
    elif (self.time + self.seconds) <= now:
      self.count = 0
      self.time = now
      return True
    else:
      return False


class AggregatorConnector:

  def __init__(self, aggregator=("127.0.0.1",5555), mode="C"):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect(aggregator)
    self.socket.sendall(mode)
    self.previous_data = ''
    self.records = 0
    self.newlines = 0

  def write(self, data):
    self.socket.sendall(data + "\n")

  def raw_read(self):
    records = []
    new_data = self.socket.recv(8000)
    data = self.previous_data + new_data
    self.newlines += data.count("\n")


    if data.count("\n") > 1:
      if data[-1] == '\n':
        for d in data.split("\n")[:-1]:
          records.append(d)
        self.previous_data = ''
      else:
        good = data.split("\n")
        for d in good[:-1]:
          records.append(d)
        self.previous_data = good[-1]
    elif data.count("\n") == 1:
      if data[-1] == '\n':
        records.append(data)
        self.previous_data = ''
      else:
        good = data.split('\n')
        records.append(good[0])
        self.previous_data = good[1]
    else:
      self.previous_data = data
    self.records += len(records)
    return records

  def json_read(self):
    #return [json.loads(line) for line in self.raw_read()]
    data = self.raw_read()
    try:
      return [json.loads(line) for line in data]
    except:
      return []


class SecondBucketCounter:
  def __init__(self, seconds):
    self.buckets = [[]]
    self.seconds = seconds
    self.previous_now = int(time.time())
  def addItem(self, item):
    now = int(time.time())
    if now == self.previous_now:
      self.buckets[-1].append(item)
    elif now == self.previous_now + 1:
      self.buckets.append([])
      self.buckets[-1].append(item)
    elif now > self.previous_now:
      for i in range(now - self.previous_now):
        self.buckets.append([])
      self.buckets[-1].append(item)
    #limit this to whatever number of seconds of watching
    if len(self.buckets) > self.seconds:
      self.buckets = self.buckets[-self.seconds:]
    self.previous_now = now
  def checkItems(self, item)
    all_connects = [item for sublist in self.buckets for item in sublist]
    if all_connects.count(item) > 150:
      command("BLOCK %s|10000\n" % item)
    print self.buckets

