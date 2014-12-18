""" Run the RepFlow testing script.
Takes 3 argument: 
    The lasting time of the experiment in SECONDS 
    desired load
    the current id"""

import os
import random
import time
import sys

FLOW_THRED = 100
PODNUM = 6

# DCTCP Distribution
# WARNING: There should be a 100KB size sample point
distsize = [0, 6, 13, 19, 33, 53, 100, 133, 667, 1333, 3333, 6667, 20000]
distpercentage = [0, 0.15, 0.2, 0.3, 0.4, 0.53, 0.58, 0.6, 0.7, 0.8, 0.9, 0.97, 1]

load = float(sys.argv[2])
avg = 0
for i in range(0, len(distsize) - 1):
  avg += (distsize[i] + distsize[i+1]) * (distpercentage[i+1] - distpercentage[i]) / 2

avg = avg * 8 / 19.5 / 1000
time_int = avg / load 
print "Average flow interval: ", time_int

#sleep time interval in seconds
TIME_INT_MAX = time_int * 1.5
TIME_INT_MIN = time_int * 0.5

PATH = os.path.dirname(os.path.realpath(__file__))

def getflowsize(sz, p):
  """ Randomly generate a flow size.
  *************INPUT************
  sz -- a list of flow size in a CDF
  p -- a list of percentage in the same CDF
  ************OUTPUT************
  size -- generated flow size (in KB) """

  points = len(distpercentage)
  #choose a value range
  rd = random.random()
  for i in range(0, points):
    if rd < distpercentage[i + 1]:
      break
  #generate the flow size
  rd = random.random()
  size = distsize[i] + rd * (distsize[i+1] - distsize[i])
  if size < 0.02:
    size = 0.02
  return size

#--------------------------------------------
# Here are the main functions
#--------------------------------------------


# cleaning
os.system("rm *.txt")
os.system("killall node")
# start self as servers
os.system("node server.js > nodeserverlog.log &")

time.sleep(3)
# Generate IP List
iplist = []
for i in range(0, PODNUM):
  for j in range(0, PODNUM/2):
    for k in range(2, PODNUM/2 + 2):
      iplist.append("10."+str(i)+"."+str(j)+"."+str(k))
myrank = int(sys.argv[3])
del iplist[myrank]
num = len(iplist)
end_time = float(sys.argv[1]) + time.time()

while time.time() < end_time:
  size = getflowsize(distsize, distpercentage)
  interval = random.random() * (TIME_INT_MAX - TIME_INT_MIN) + TIME_INT_MIN
  server = iplist[random.randrange(num)]
  time.sleep(interval)
  # print "Sending Flow Size: %f KBytes After %f ms" % (size, interval*1000)

  # if it is a large flow, initiate an iperf client
  if size > FLOW_THRED:
    os.system("node client.js " + str(size) + " " + server + " > longflowlog.log &")
  # if it is a small flow
  else:
    flag_rep = 3 * random.random()
    if flag_rep < 4:
      os.system("node client.js " + str(size) + " " + server &")
    elif flag_rep < 2:
      os.system("node repflow.js " + str(size) + " " + server + " >> " + str(myrank) + "rep.txt &")
    else:
      os.system("node repsyn.js " + str(size) + " " + server + " >> " + str(myrank) + "repsyn.txt &")
  
os.system("rm *.log")
time.sleep(3)
