#!/usr/bin/node

var net = require('net');

clients = []
servers = []

//console.log(clients);

function bye(c) {
 if (clients.indexOf(c) > -1) {
    index = clients.indexOf(c);
    clients.splice(index, 1);
    //console.log("Clients: " + clients.length);
  } else if (servers.indexOf(c) > -1) {
    index = servers.indexOf(c);
    servers.splice(index, 1);
    //console.log("Servers: " + servers.length);
  }
};

server = net.createServer(function(c) {
  oldData = '';
  c.on('data', function(data) {
    //console.log(data.toString().trim());
    if (data.toString().trim() == 'S') {
      servers.push(c);
      //console.log(servers.length);
    } else if (data.toString().trim() == 'C') {
      clients.push(c);
      //console.log(clients.length);
    } else {
      if (data.toString()[data.length-1] == '\n') {
        allData = oldData + data;
        if (oldData != '') {
          console.log("fixed some data");
          console.log(allData.length);
        }
        oldData = '';
        //console.log ('complete data ' + data.length );
        if (servers.indexOf(c) > -1) {
          clients.forEach(function (sock) {
            sock.write(allData);
          })
        } else if (clients.indexOf(c) > -1) {
          servers.forEach(function (sock) {
            sock.write(allData);
          });
        } else {
          c.write('Servers: ' + servers.length + "\nClients: " + clients.length + "\n");
        };
      } else {
        oldData = oldData + data
        //console.log ('incomplete data ' + data.length );
        //console.log(data.toString());
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
