# The documentation is sparse, will improve this next:

## Proxy

Usage: /usr/bin/node ./proxy.js -o [loghost] -P [logport] -t [target_host] -p [target_port] -l [proxy_listen_port]

Options:
  -t  [required]
  -p  [required]
  -l  [required]
  -o  [default: "localhost"]
  -P  [default: 5555]

## Aggregator


Usage /usr/bin/node ./aggregator.js  -l [listen_port]


Dependencies:
npm install http-proxy
npm install uuid
npm install optimist

Optional:
npm install forever
