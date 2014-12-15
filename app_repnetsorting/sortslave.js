// Slave Program for Bucket Sorting

var net = require('net');
var repnet = net;
// var repnet = require('../repnet/repnet');
var fs = require('fs');
var readline = require('readline');

var workernum = 6; // number of available machines
var my_id; // local machine id
var UPPERBOUND = 6000;
var LOWERBOUND = 0;

var iplist = fs.readFileSync('iplist').toString();
iplist = iplist.split('\n');
my_id = Number(iplist[0]);

var my_lowerbound = (UPPERBOUND - LOWERBOUND) / workernum * ((my_id - 1) % workernum) + LOWERBOUND;
var counterlength = (UPPERBOUND - LOWERBOUND) / workernum;

// CounterDict (masterID: Counter Object)
function Dictionary () {
  this.key = [];
  this.value = [];
  this.indexOf = function (searchkey) {
    return this.key.indexOf(searchkey);
  };
  this.newElem = function (newkey, newvalue) {
    this.key.push(newkey);
    this.value.push(newvalue);
    return this.key.indexOf(newkey);
  };
  this.getValue = function (searchkey) {
    return this.value[this.key.indexOf(searchkey)];
  };
  this.deletekey = function (searchkey) {
    var index = this.key.indexOf(searchkey);
    this.key.splice(index, 1);
    this.value.splice(index, 1);
    return 0;
  };
}

var CounterDict = new Dictionary();

// counter class
function Counter (masterID, lowerbound) {
  this.master = masterID;
  this.lbound = lowerbound;
  this.count = [];
  this.masterIP = "192.168.";
  if (this.master > 6) {
    this.masterIP += "7.";
    this.masterIP += (this.master - 6).toString();
  }
  else {
    this.masterIP += ("6." + this.master.toString());
  }
  for (var i = 0; i < counterlength; i++) {
    this.count.push(0);
  }
  // newnumber function, count a newly got number "num"
  this.newnumber = function (num) {
    num = num - this.lbound;
    this.count[num]++;
  };
  // notification function, notify master at port 5700
  this.notification = function () {
    var not = repnet.createConnection(5700, this.masterIP, function () {
      var buf = new Buffer(2);
      var workerid = my_id;
      if (my_id > 6) workerid -= 6;
      buf.writeInt16LE(workerid, 0);
      not.write(buf);
      not.end();
    });
  };
  // sendresult function, send the entire result to the master
  this.sendresult = function (conn) {
    var result = "";
    for (var i = 0; i < counterlength; i++) {
      for (var j = 0; j < this.count[i]; j++) {
        result += ((lowerbound + i).toString() + '\n');
      }
    }
    var buf = new Buffer(result);
    conn.write(buf);
    conn.end();
    console.log("Returning Result to Master " + this.masterIP);
    CounterDict.deletekey(this.master);
  };
}

var SlaveSorter = repnet.createServer(function(conn) {
  conn.on('data', function(data){
    var master = data.readInt16LE(0);
    var total = data.readInt16LE(2);
    var cnt; // current Counter instance
    if (CounterDict.indexOf(master) < 0) { // new master
      cnt = new Counter(master, my_lowerbound);
      CounterDict.newElem(master, cnt);
    }
    else {
      cnt = CounterDict.getValue(master);
    }
    if (total === 0) { // end of message
      cnt.notification();
    }
    else { // new data
      var payload = data.toString('utf8', 4);
      var numbers = payload.split(',');
      for (var i = 0; i < numbers.length; i++) {
        cnt.newnumber(Number(numbers[i]));
      }
    }
  });
});
SlaveSorter.listen(5600, function (){});

// Result Disseminator, listening on 5800
var ResultDisseminator = net.createServer(function (query) {
  var master;
  query.on('data', function (data) {
    master = data.readInt16LE(0);
    debugger;
    var currentCounter = CounterDict.getValue(master);
    currentCounter.sendresult(query);
  });
});
ResultDisseminator.listen(5800);

