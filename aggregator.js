#!/usr/bin/node

var net = require('net');

clients = []
servers = []
commandOnlyClients = []

/** Function count the occurrences of substring in a string;
 * @param {String} string   Required. The string;
 * @param {String} subString    Required. The string to search for;
 * @param {Boolean} allowOverlapping    Optional. Default: false;
 */
function occurrences(string, subString, allowOverlapping){

    string+=""; subString+="";
    if(subString.length<=0) return string.length+1;

    var n=0, pos=0;
    var step=(allowOverlapping)?(1):(subString.length);

    while(true){
        pos=string.indexOf(subString,pos);
        if(pos>=0){ n++; pos+=step; } else break;
    }
    return(n);
}

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
  c.oldData = '';
  c.on('data', function(data) {
    if (data.length > 4) {
      data = data.toString()
      if (data[data.length-1] == '\n') {
        //assembles data into full size chunks
        allData = c.oldData + data;
        c.oldData = '';
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
        c.oldData = c.oldData + data
      };

    } else if (data.toString().trim() == 'S') {
      servers.push(c);
    } else if (data.toString().trim() == 'C') {
      clients.push(c);
    } else if (data.toString().trim() == 'CO') {
      commandOnlyClients.push(c);
    } else {
      data = data.toString()
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
