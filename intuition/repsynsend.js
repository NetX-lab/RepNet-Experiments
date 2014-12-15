var net = require('net');

var flag = false;
var buf = Buffer(102400);
var t0 = process.hrtime();
var t1;
var client1 = net.connect(8888, '192.168.7.1', function() {
  if (!flag){ 
    flag = true;
    client1.write(buf);
    client1.on('end', function() {
      t1 = process.hrtime(t0);
      console.log((t1[0] * 1e3 + t1[1] / 1e6).toString());
    });
  }
  client1.end();
});

var client2 = net.connect(8888, '192.168.7.1', function() {
  if (!flag){ 
    flag = true;
    client2.write(buf);
    client2.on('end', function() {
      t1 = process.hrtime(t0);
      console.log((t1[0] * 1e3 + t1[1] / 1e6).toString());
    });
  }
  client2.end();
});
 
