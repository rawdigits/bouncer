#!/usr/bin/node

var http = require('http');
var httpProxy = require('http-proxy');

var net = require('net');

setInterval(function() {
  console.log('hi')
  },5000);


http.createServer(function(req, res) {
  res.end('hello world\n');
  }).listen(8080);
