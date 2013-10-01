#!/usr/bin/python

import time
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

now = int(time.time())
hosts = ["%s-hosts" % x for x in range(now-600, now)]
seconds = ["%s" % x for x in range(now-600, now)]
#for second in range(now-60, now):
r.zunionstore('hosts',hosts)

total = 0
for second in seconds:
  try:
    total += int(r.get(second))
  except:
    pass
print total

#print second
