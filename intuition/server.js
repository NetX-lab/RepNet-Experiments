var net = require('net');

var server = net.createServer(function(c) {
  c.on('data', function(buffer) {});
  c.on('end', function() {
    c.end();
  });
});

server.listen(8888);
