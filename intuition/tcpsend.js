var net = require('net');

var buf = Buffer(102400);
var t0 = process.hrtime();
var t1;
var client = net.connect(8888, '192.168.7.1', function() {
  client.write(buf);
  client.end();
});

client.on('end', function() {
  t1 = process.hrtime(t0);
  console.log((t1[0] * 1e3 + t1[1] / 1e6).toString());
});
