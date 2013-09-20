import simplejson as json
import socket
import time

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
