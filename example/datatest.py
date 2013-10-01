#!/usr/bin/python

#{u'host': u'10.0.10.150', u'type': u'connect'}

#{u'uuid': u'edc606fe-4943-4eb1-9778-bd2504c4fb79', u'url': u'/changelog/', u'headers': {u'cookie': u'__utma=140242144.1351725976.1379689985.1379689985.1379689985.1; __utmb=140242144.21.10.1379689985; __utmc=140242144; __utmz=140242144.1379689985.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); kvcd=1379691705286; km_ai=KZ88gu2f5TXoaf3yEzD%2F5JOzQmo%3D; km_uq=; km_vs=1; km_lv=1379691705; _mkto_trk=id:958-PRK-049&token:_mch-risk.io-1379689986414-35976; __ar_v4=ZUIXVDTSPBGNDBCXJFDXCR%3A20130920%3A20%7C2T4HRKJGUBEBPODPNBD5IJ%3A20130920%3A20%7CVOZ53KQPSBGS7I3CBGPHK3%3A20130920%3A20', u'accept-language': u'en-US,en;q=0.5', u'accept-encoding': u'gzip, deflate', u'x-forwarded-port': 63139, u'x-forwarded-for': u'10.0.10.150', u'connection':u'keep-alive', u'accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'user-agent': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0', u'host': u'blog.risk.io', u'x-forwarded-proto': u'http', u'referer': u'http://blog.risk.io/', u'x-moz': u'prefetch'}, u'host': u'10.0.10.150', u'time': 1379691895755, u'type': u'request', u'method': u'GET'}

import shared
import random
import uuid
import simplejson as json
import sys
import time

fake_paths = ['/blog','/buystuff','/somepath']

def fake_ips(count):
  for each in range(count):
    yield "%s.%s.%s.%s" % tuple([int(random.random() * 254) + 1 for x in range(4)])

fake_hosts = [x for x in fake_ips(10000)]


class MockHttp:
  def __init__(self):
#    self.host = fake_ips()
    self.time = int(time.time() * 1000)
    #self.method = 'GET'
  def request(self):
    #this enables random ip
    self.method = "GET\n"
    self.type = 'request'
    self.uuid = str(uuid.uuid4())
    self.url = fake_paths[int(random.random() * len(fake_paths))]
    self.host = fake_hosts[int(random.random() * len(fake_hosts))]
    self.time = int(time.time() * 1000)
    return(json.dumps(self.__dict__))
  def connect(self):
    return(json.dumps({"host":self.host,"uuid":self.uuid,"type": "connect"}))
  def end(self):
    return(json.dumps({"host":self.host,"uuid":self.uuid,"type": "end"}))

agg = shared.AggregatorConnector(mode="S")

m = MockHttp()
for i in range(0,int(sys.argv[1])):
  connect = str(m.request())
  agg.write(connect)
  time.sleep(.0001)
#  agg.write(str(m.request()))
  #time.sleep(.1)
#  agg.write(str(m.end()))
#  del(m)
