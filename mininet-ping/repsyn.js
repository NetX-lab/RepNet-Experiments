//*****************************
// Exact Three Parameters
// 1: (float) flow size in KBytes
// 2: (string) server hostname
//*****************************

// Client behavour:
// 1. establish an connection and start timing
// 2. semd a bunch of data
// 3. send out FIN immediately after the data are all sent out.
// 4. stop timing as soon as the FIN is received.
// OUTPUT (two numbers): <FCT in ms>  <flow size>

var net = require('net');

var size = Math.ceil(process.argv[2] * 1024);
var host = process.argv[3];

function Client(p, h)
{
  var t0, t1;
  var data = new Buffer(size);
  var flag = 0;

  var client = net.connect(p, h, function() { //'connect' listener
    if (flag === 0) {
      flag = 1;
      t0 = process.hrtime();
      client.write(data);
    }
    client.end();
  });
  var client1 = net.connect(p, h, function() { //'connect' listener
    if (flag === 0) {
      flag = 2;
      t0 = process.hrtime();
      client1.write(data);
    }
    client1.end();
  });

  // when 'end' event is emitted, all message has been received.
  client.on('end', function() {
    if (flag == 1) {
      t1 = process.hrtime(t0);
      console.log(t1[0]*1000 + t1[1]/1000000, size);
    }
  });
  client1.on('end', function() {
    if (flag == 2) {
      t1 = process.hrtime(t0);
      console.log(t1[0]*1000 + t1[1]/1000000, size);
    }
  });
  client.on('error', function(e) {client.destroy(); 
            //console.log("repsyn error!");
  });
  client1.on('error', function(e) {client1.destroy(); //console.log("repsyn error!");
  });
}

client = new Client(5337, host);
