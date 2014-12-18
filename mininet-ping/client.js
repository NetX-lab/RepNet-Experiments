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

  var client = net.connect(p, h, function() { //'connect' listener
    t0 = process.hrtime();
    client.write(data);
    client.end();
  });

  // when 'end' event is emitted, all message has been received.
  client.on('end', function() {
    t1 = process.hrtime(t0);
    console.log(t1[0]*1000 + t1[1]/1000000, size);
  }); 
  client.on('error', function(e) {client.destroy(); //console.log("client error!");
  });
}

client = new Client(5337, host);
