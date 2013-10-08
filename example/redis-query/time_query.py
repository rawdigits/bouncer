#!/usr/bin/python

from datetime import datetime
from time import mktime
import time
import redis
import sys

start_date = int(mktime(time.strptime(sys.argv[1], "%Y-%m-%d-%H:%M:%S")))

if len(sys.argv) <= 2:
  end_date = int(time.time())
else:
  end_date = int(mktime(time.strptime(sys.argv[2], "%Y-%m-%d-%H:%M:%S")))


r = redis.StrictRedis(host='localhost', port=6379, db=0)

now = int(time.time())
hosturls = ["%s-hosturls" % x for x in range(start_date, end_date)]
print hosturls
hosts = ["%s-hosts" % x for x in range(start_date, end_date)]
urls = ["%s-urls" % x for x in range(start_date, end_date)]
useragents = ["%s-useragents" % x for x in range(start_date, end_date)]
seconds = ["%s" % x for x in range(start_date, end_date)]

#for second in range(now-60, now):
r.zunionstore('hosturls',hosturls)
r.zunionstore('hosts',hosts)
r.zunionstore('urls',urls)
r.zunionstore('useragents',useragents)

total = 0
for second in seconds:
  try:
    total += int(r.get(second))
  except:
    pass
print total
print

for ip in r.zrevrange('hosts',0,10, withscores=True):
  print ip
print

for ip in r.zrevrange('useragents',0,10, withscores=True):
  print ip
print

for ip in r.zrevrange('urls',0,10, withscores=True):
  print ip
print

for ip in r.zrevrange('hosturls',0,10, withscores=True):
  print ip

#print second
