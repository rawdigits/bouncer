#!/usr/bin/node

var net = require('net');

clients = []
servers = []
commandOnlyClients = []


function bye(c) {
 if (clients.indexOf(c) > -1) {
    index = clients.indexOf(c);
    clients.splice(index, 1);
  } else if (servers.indexOf(c) > -1) {
    index = servers.indexOf(c);
    servers.splice(index, 1);
  }
};

server = net.createServer(function(c) {
  oldData = '';
  c.on('data', function(data) {
    if (data.toString().trim() == 'S') {
      servers.push(c);
    } else if (data.toString().trim() == 'C') {
      clients.push(c);
    } else if (data.toString().trim() == 'CO') {
      commandOnlyClients.push(c);
    } else {
      if (data.toString()[data.length-1] == '\n') {
        //assembles data into full size chunks
        allData = oldData + data;
        oldData = '';
        if (servers.indexOf(c) > -1) {
          clients.forEach(function (sock) {
            sock.write(allData);
          })
        } else if (clients.indexOf(c) > -1) {
          servers.forEach(function (sock) {
            sock.write(allData);
          });
        } else if (commandOnlyClients.indexOf(c) > -1) {
          servers.forEach(function (sock) {
            sock.write(allData);
          });
        } else {
          c.write('Servers: ' + servers.length + "\nClients: " + clients.length + "Command only Clients: " + commandOnlyClients.length + "\n");
        };
      } else {
        oldData = oldData + data
      };
    };
  });
  c.on('end', function() {
    bye(c);
  });
  c.on('error', function() {
    c.end();
    bye(c);
  });

});

server.listen(5555);
