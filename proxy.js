#!/usr/bin/node

var http = require('http');
http.globalAgent.maxSockets = 100000
var httpProxy = require('http-proxy');
var uuid = require('uuid');
var net = require('net');

//CONSTANTS
var UPSTREAM_LOGSERVER = process.argv[2];
var HTTP_SERVER = process.argv[3];
var HTTP_PORT = process.argv[4];
var PROXY_PORT = process.argv[5];
//#TODO: add support for behind proxy

//GLOBALs
var upstreamConnection;
var blacklist = {};
var sweeplist = [];
var greylist = {};
var connections = [];
var requests = [];
var disabledUrls = [];
var totalConnections = 0;
var headerTimeout = 120000;
var requestTimeout = 120000;

process.setMaxListeners(0);

//Incoming commands from upstream server
function commandDo(cmd) {
  cmd = cmd.toString().trim().toLowerCase();
  if (/^block.*/.test(cmd)) {
    cmd = cmd.slice(6).split("|")
    timeToBlock =  new Date().getTime() + parseInt(cmd[1]);
    sweeplist.push(cmd[0]);
    blacklist[cmd[0]] = timeToBlock;
  } else if (/^grey.*/.test(cmd)) {
    cmd = cmd.slice(5).split("|")
    timeToBlock =  new Date().getTime() + parseInt(cmd[1]);
    greylist[cmd[0]] = timeToBlock;
  } else if (/^rtimeout.*/.test(cmd)) {
    requestTimeout = parseInt(cmd.slice(9));
  } else if (/^htimeout.*/.test(cmd)) {
    headerTimeout = parseInt(cmd.slice(9));
  } else if (/^durl.*/.test(cmd)) {
    disabledUrls.push(cmd.slice(5));
  } else if (/^eurl.*/.test(cmd)) {
    disabledUrls.splice(disabledUrls.indexOf(cmd.slice(5)));
  } else if (/^unblock.*/.test(cmd)) {
    cmd = cmd.slice(8)
    delete blacklist[cmd];
  } else if (cmd == "flush") {
    return blacklist = {};
  } else if (cmd == "kill") {
    cmd = cmd.slice(5)
    //connections
  };
}

function buildRequestMessage(req) {
  message = {};
  message.time    = new Date().getTime();
  message.type    = "request";
  message.host    = req.socket.remoteAddress;
  message.url     = req.url;
  message.method  = req.method;
  message.headers = req.headers;
  message.uuid    = req.uuid;
  return JSON.stringify(message);
}

function buildConnectMessage(req) {
  message = {};
  message.type    = "connect";
  message.host    = req.remoteAddress;
  return JSON.stringify(message);
}

function buildEndMessage(req) {
  message = {};
  message.time    = new Date().getTime();
  message.type    = "end";
  message.host    = req.remoteAddress;
  message.uuid    = req.uuid;
  return JSON.stringify(message);
}

function checkBlacklist(addr) {
  if (addr in blacklist) {
    if (blacklist[addr] > new Date().getTime()) {
      return false;
    } else {
      delete blacklist[addr];
      return true;
    }
  } else {
    return true;
  }
}

function checkGreylist(addr,url) {
  if (addr in greylist) {
    if (greylist[addr] > new Date().getTime()) {
      return checkDisabledUrls(url)
    } else {
      delete greylist[addr];
      return true;
    }
  } else {
    return true;
  }
}


function checkDisabledUrls(url) {
  url = url.split("?")[0]
  if (disabledUrls.indexOf(url) > -1) {
    return false;
  } else { return true; }
}

//This connects to the aggregation server and accepts upstream commands.
setInterval(function() {
  if (!upstreamConnection || upstreamConnection == null) {
    upstreamConnection = net.connect({host: UPSTREAM_LOGSERVER, port: 5555})
    //connect to aggregator in "server" mode
    upstreamConnection.write('S');
    upstreamConnection.on('data', function(data) {
      commandDo(data);
    });
    //destroys upstream if the connection is dead
    upstreamConnection.on('error', function () {
      return upstreamConnection = null
    });
  };
},1000);

//this is an aggregator ping  if there are no incoming conns this fixes upstream
setInterval(function() {
  try {
    upstreamConnection.write('P');
  } catch (e) {}
},2000);

setInterval(function() {
  requests.forEach(function (req) {
    if ((req.startTime + requestTimeout) < new Date().getTime()) {
      requests.splice(requests.indexOf(req),1);
      req.socket.end();
    };
  });
},250);

setInterval(function() {
  connections.forEach(function (req) {
    if ((req.startTime + headerTimeout) < new Date().getTime()) {
      connections.splice(connections.indexOf(req),1);
      req.end();
    };
  });
},250);

//TODO: make this work properly
//Sweep newly blacklisted servers right away
setInterval(function() {
  if (sweeplist.length > 0 && requests.length > 0) {
      requests.forEach(function (req) {
        if (sweeplist.indexOf(req.socket.remoteAddress) > -1) {
          req.socket.end();
          requests.splice(requests.indexOf(req),1);
        };
      });
  } return sweeplist = [];
} ,1000);

proxy = new httpProxy.RoutingProxy();
//proxyServer = httpProxy.createServer(function (req, res, proxy) {
proxyServer = http.createServer(function (req, res) {
  //this important bit helps against slowloris
  //req.setTimeout(12000);
  if (checkBlacklist(req.socket.remoteAddress) && checkGreylist(req.socket.remoteAddress,req.url)) {
    totalConnections += 1;
    proxy.proxyRequest(req, res, {
    host: HTTP_SERVER,
    port: HTTP_PORT
    });
    req.uuid = uuid.v4();
    //id = uuid.v4();
    try {
    upstreamConnection.write(buildRequestMessage(req) + "\n");
    } catch (e) {}
  } else {
    req.connection.write('disabled');
    req.connection.end();
  }
}).listen(PROXY_PORT);

proxyServer.on('request', function (req, res) {
  //remove good requests from garbage collection
  req.startTime = new Date().getTime();
  requests.push(req);
  connections.splice(connections.indexOf(req),1);
});

proxyServer.on('connection', function (req, c, h) {
  //mark the start time vs slow laris
  if (checkBlacklist(req.remoteAddress)) {
    req.startTime = new Date().getTime();
    connections.push(req);
    try {
      upstreamConnection.write(buildConnectMessage(req) + "\n");
    } catch (e) {}
  } else {
    req.end()
  }
});

proxy.on('end', function (req) {
  //upstreamConnection.write(req.id + "ENDDDDDDDD\n");
  requests.splice(requests.indexOf(req),1);
  try {
    upstreamConnection.write(buildEndMessage(req) + "\n");
  } catch (e) {}
});

proxy.on('error', function(proxy) {
  //totalConnections -= 1;
  try {
  upstreamConnection.write(buildEndMessage(req) + "\n");
  } catch (e) {}
  //c = connections.indexOf(proxy);
  //connections.splice(c, 1);
});

//proxy.on('end', function(proxy) {
//  totalConnections -= 1;
//  //c = connections.indexOf(proxy);
//  //connections.splice(c, 1);
//});
