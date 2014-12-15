var net = require('net');

var flag = false;
var t0 = process.hrtime();
var t1;
var client = net.connect(8888, '192.168.7.1', function() {
  if (!flag) {
    flag = true;
    t1 = process.hrtime(t0);
    console.log((t1[0] * 1e3 + t1[1] / 1e6).toString());
  }
  client.end();
});
var client1 = net.connect(8888, '192.168.7.1', function() {
  if (!flag) {
    flag = true;
    t1 = process.hrtime(t0);
    console.log((t1[0] * 1e3 + t1[1] / 1e6).toString());
  }
  client1.end();
});
