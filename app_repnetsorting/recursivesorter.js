// The recursive bucket sorter, not completed

var net = require('net');
var repnet = net;

var fs = require('fs');
var readline = require('readline');

var workernum = 12; // number of available machines
var my_id; // local machine id
var current_depth = 0;
var UPPERBOUND = 120000;
var LOWERBOUND = 0;

function id2ip(id) {
  var ipaddr = "192.168.";
  if (ipaddr < 7) {
    ipaddr = ipaddr + "6" + id.toString();
  }
  else {
    id = id - 6;
    ipaddr = ipaddr + "7" + id.toString();
  }
  return ipaddr;
}

var Sorter = function(filename, depth, fromMachine, upper, lower){
  // Initiate the locol Bucket for Buffering
  var Bucket = [];
  var BucketCount = [];
  for (var i = 0; i < workernum; i++) {
    Bucket.push([]);
    BucketCount.push(0);
  }
  // Readfile, find out if job can be done locally
  var linereader = readline.createInterface({
    input: fs.createReadStream(filename),
    output: process.stdout,
    terminal: false
  });
  linereader.on('line', function(line) {
    var flag_localsort = false;
  });

  var Count_CompleteWorker = workernum; // Decreasing Counter indicating progress
  var ProgressMonitor = net.createServer(function(c) {
    Count_CompleteWorker--;
    c.end();
    if (Count_CompleteWorker === 0) {
      ProgressMonitor.close();
      // Start Result Collector Here ******
    }
  });
  ProgressMonitor.listen(5600 + depth, function() {
    console.log('Progress Monitor Online for Depth ' + depth.toString());
  });
};
