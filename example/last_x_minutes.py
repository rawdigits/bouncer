#!/usr/bin/python

import time
import redis

minutes_ago = sys.argv[1]

r = redis.StrictRedis(host='localhost', port=6379, db=0)

now = int(time.time())
hosturls = ["%s-hosturls" % x for x in range(now-minutes_ago, now)]
hosts = ["%s-hosts" % x for x in range(now-minutes_ago, now)]
urls = ["%s-urls" % x for x in range(now-minutes_ago, now)]
seconds = ["%s" % x for x in range(now-minutes_ago, now)]

#for second in range(now-60, now):
r.zunionstore('hosturls',hosturls)
r.zunionstore('hosts',hosts)
r.zunionstore('urls',urls)

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

for ip in r.zrevrange('urls',0,10, withscores=True):
  print ip
print

for ip in r.zrevrange('hosturls',0,10, withscores=True):
  print ip

#print second
