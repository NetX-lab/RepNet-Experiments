var net = require('net');

var t0 = process.hrtime();
var t1;
var client = net.connect(8888, '192.168.7.1', function() {
  t1 = process.hrtime(t0);
  console.log((t1[0] * 1e3 + t1[1] / 1e6).toString());
  client.end();
});
