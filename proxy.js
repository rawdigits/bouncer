#!/usr/bin/node

var http = require('http');
var httpProxy = require('http-proxy');
var net = require('net');

//CONSTANTS
var UPSTREAM_LOGSERVER = process.argv[2];

var upstreamConnection;


setInterval(function() {
  if (!upstreamConnection) {
//  try {
    upstreamConnection = net.connect({port: 8222}, function() {
    console.log("Connected");
//      console.log('connected')
      });
  };
//  } catch (e) {console.log('hi')};
},1000);

setInterval(function() {
  upstreamConnection.write("TEST\n");

},2000);



http.createServer(function(req, res) {
  res.end('hello world\n');
}).listen(8080);
