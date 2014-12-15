// Master Program for Bucket Sorting

var net = require('net');
var repnet = net;
// var repnet = require('../repnet/repnet');
var fs = require('fs');
var readline = require('readline');

// Start Timer
var t0 = process.hrtime();
var t1;

var workernum = 6; // number of available machines
var my_id; // local machine id
var UPPERBOUND = 6000;
var LOWERBOUND = 0;
try {
  fs.unlinkSync("./SortedNumbers.dat");
}
catch (err) {}

var iplist = fs.readFileSync('iplist').toString();
iplist = iplist.split('\n');
my_id = Number(iplist[0]);

// Initiate the locol Bucket for Buffering
var Bucket = [];
var Boundary = []; // Upper Bound to compare
var ProgressIndicator = []; // a list of flag indicating job done or not
var list;

for (var i = 1; i < workernum + 1; i++) {
  (function (temp) {
    Bucket.push([]);
    ProgressIndicator.push(false);
    Boundary.push((UPPERBOUND - LOWERBOUND) / workernum * (temp - 1) + LOWERBOUND);
  }
)(i)};

// Function Flush Bucket, make it a sync process
function FlushBucket (target, number) {
  var payload = new Buffer(Bucket[target - 1].toString());
  Bucket[target - 1] = [];
  var buf = new Buffer(4 + payload.length);
  buf.writeInt16LE(my_id, 0);
  buf.writeInt16LE(number, 2);
  payload.copy(buf, 4);
  var client = repnet.createConnection(5600, iplist[target], function(){
    client.write(buf);
    client.end();
  });
  return number;
}

(function (){
  var data;
  data = fs.readFileSync('./numbers.dat', {encoding: 'utf8'});
  list = data.split('\n');
  list.pop();
  for (var i = 0; i < list.length; i++) {
    (function(index){
      var j = 0;
      for (j = 0; j < workernum; j++) {
        if (list[index] < Boundary[j]) break;
      }
      (function(target){
        Bucket[target - 1].push(list[index]);
        if (Bucket[target - 1].length >= 20) {
          FlushBucket(target, Bucket[target - 1].length);
        }
      })(j);
    })(i);
  }
  // All Done
  for (var i = 1; i < workernum + 1; i++) {
    (function (target){
      if (Bucket[target - 1].length > 0) {
        FlushBucket(target, Bucket[target - 1].length);
      }
      FlushBucket(target, 0);
    }) (i);
  }
})();

var ProgressMonitor = repnet.createServer(function(c) {
  c.on('end', function (){
    c.end();
  });
  c.on('data', function (data){
    var workerdone = data.readInt16LE(0);
    (function (index){
      var QueryResult = net.createConnection(5800, iplist[index], function () {
        console.log("Query Result From Woker No." + index.toString());
        var buf = new Buffer(2);
        buf.writeInt16LE(my_id, 0);
        QueryResult.write(buf);
        QueryResult.on('end', function() {
          QueryResult.end();
        });
        QueryResult.on('data', function(sortednumbers) {
          debugger;
          fs.appendFileSync('./temp' + index.toString(), sortednumbers.toString());
          console.log("Caching: result from " + index.toString());
          ProgressIndicator[workerdone - 1] = true;
          while (ProgressIndicator[ProgressMonitor.collectedIndex] === true){
            ProgressMonitor.collectedIndex++;
            (function (current) {
              fs.appendFileSync('./SortedNumbers.dat', fs.readFileSync('./temp' + current.toString()));
              fs.unlinkSync('./temp' + current.toString());
              console.log("Writing: result from " + current.toString());
              return 0;
            })(ProgressMonitor.collectedIndex);
            if (ProgressMonitor.collectedIndex === workernum) {
              t1 = process.hrtime(t0);
              console.log((t1[1] / 1000000 + t1[0] * 1000).toString());
              fs.appendFileSync('./time' + my_id + '.dat', (t1[1] / 1000000 + t1[0] * 1000).toString() + "\n");
              ProgressMonitor.close();
              break;
            }
          }
        });
      });
    })(workerdone);
  });
});
ProgressMonitor.collectedIndex = 0;
ProgressMonitor.listen(5700, function () {});

