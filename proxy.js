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
var assholes = {};
var connections = [];
var reqs = [];
var totalConnections = 0;
var headerTimeout = 10000;

process.setMaxListeners(0);

//Incoming commands from upstream server
function commandDo(cmd) {
  cmd = cmd.toString().trim().toLowerCase();
  if (/^block.*/.test(cmd)) {
    cmd = cmd.slice(6).split("|")
    timeToBlock =  new Date().getTime() + parseInt(cmd[1]);
    assholes[cmd[0]] = timeToBlock;
  } else if (/^unblock.*/.test(cmd)) {
    cmd = cmd.slice(8)
    delete assholes[cmd];
  } else if (cmd == "flush") {
    return assholes = {};
  } else if (cmd == "kill") {
    cmd = cmd.slice(5)
    //connections
  };
}

function buildMessage(req, uuid) {
  message = {};
  message.host    = req.socket.remoteAddress;
  message.url     = req.url;
  message.method  = req.method;
  message.headers = req.headers;
  message.uuid    = uuid;
  return JSON.stringify(message);
}

function checkRequest(req) {
  if (req.socket.remoteAddress in assholes) {
    if (assholes[req.socket.remoteAddress] > new Date().getTime()) {
      console.log('found asshole');
      req.connection.end();
      return false;
    } else {
      delete assholes[req.socket.remoteAddress];
      return true;
    }
  } else {
    return true;
  }
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

setInterval(function() {
  reqs.forEach(function (req) {
    if ((req.startTime + headerTimeout) < new Date().getTime()) {
      reqs.splice(reqs.indexOf(req),1);
      req.end();
    };
  });
  //console.log(reqs.length);
},1000);


proxy = new httpProxy.RoutingProxy();
//proxyServer = httpProxy.createServer(function (req, res, proxy) {
proxyServer = http.createServer(function (req, res) {
  //this important bit helps against slowloris
  //console.log(req);
  req.setTimeout(12000);
  if (checkRequest(req)) {
    totalConnections += 1;
    proxy.proxyRequest(req, res, {
    host: HTTP_SERVER,
    port: HTTP_PORT
    });
    id = uuid.v4();
    try {
    upstreamConnection.write(buildMessage(req, id) + "\n");
    } catch (e) {}
  }
}).listen(PROXY_PORT);

proxyServer.on('request', function (req, res) {
  //remove good requests from garbage collection
  reqs.splice(reqs.indexOf(req),1);
});

proxyServer.on('connection', function (req, c, h) {
  //mark the start time vs slow laris
  req.startTime = new Date().getTime();
  reqs.push(req);
});

proxy.on('error', function(proxy) {
  totalConnections -= 1;
  //c = connections.indexOf(proxy);
  //connections.splice(c, 1);
});

proxy.on('end', function(proxy) {
  totalConnections -= 1;
  //c = connections.indexOf(proxy);
  //connections.splice(c, 1);
});
