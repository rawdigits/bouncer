#!/usr/bin/node

var http = require('http');
var httpProxy = require('http-proxy');
var net = require('net');

//CONSTANTS
var UPSTREAM_LOGSERVER = process.argv[2];

var upstreamConnection;
var assholes = {};


function commandDo(cmd, assholes) {
  cmd = cmd.toString().trim().toLowerCase();
  if (/block.*/.test(cmd)) {
    cmd = cmd.slice(6).split("|")
    assholes[cmd[0]] = cmd[1];
    console.log(cmd);
  } else if (cmd == "clear") {
    assholes = {};
    console.log("Clearing stored list.");
  } else if (cmd == "show") {
    console.log(assholes);
  };
}


setInterval(function() {
  if (!upstreamConnection) {
    upstreamConnection = net.connect({port: 8222});
    upstreamConnection.on('data', function(data) {
      commandDo(data, assholes);
    });
    upstreamConnection.on('error', function () {
      upstreamConnection = null;
    });
  };
},1000);

setInterval(function() {
  try {
    //upstreamConnection.write("TEST\n");
  } catch (e) {};

},2000);




http.createServer(function(req, res) {
  res.end('hello world\n');
}).listen(8080);
