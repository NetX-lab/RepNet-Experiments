import os

serverA = open('serverlistA.list', 'r')
serverB = open('serverlistB.list', 'r')
numA = int(serverA.readline())
numB = int(serverB.readline())

iplistA = open('iplistA', 'w')
iplistB = open('iplistB', 'w')

sshconfig = open('/Users/iqua/.ssh/config', 'w')
csshconfig = open('/etc/clusters', 'w')

csshconfig.write("rackA ")
for i in range(numA):
  port = int(serverA.readline())
  content = "host A" + str(port) + "\n  Hostname sing.cse.ust.hk\n  User shuhao\n  Port " + str(port) + "\n"
  sshconfig.write(content)
  hostname = "A" + str(port) + " "
  csshconfig.write(hostname)
  ipaddr = "192.168.6." + str(port - 30042) + "\n"
  iplistA.write(ipaddr)
iplistA.close()

csshconfig.write("\nrackB ")
for i in range(numB):
  port = int(serverB.readline())
  content = "host B" + str(port) + "\n  Hostname sing.cse.ust.hk\n  User shuhao\n  Port " + str(port) + "\n"
  sshconfig.write(content)
  hostname = "B" + str(port) + " "
  csshconfig.write(hostname)
  if (port == 30055):
    port = 30050
  ipaddr = "192.168.7." + str(port - 30048) + "\n"
  iplistB.write(ipaddr)
iplistB.close()

# sshconfig.write("host B30054\n  Hostname sing.cse.ust.hk\n  User shuhao\n  Port 30054\n");
# sshconfig.write("host A30048\n  Hostname sing.cse.ust.hk\n  User shuhao\n  Port 30048\n");

sshconfig.close()
csshconfig.close()
serverA.close()
serverB.close()

csshconfig = open('/etc/clusters', 'r')
serverA = csshconfig.readline().split()
serverB = csshconfig.readline().split()
csshconfig.close()

for i in range(1, numA+1):
  os.system("echo '" + str(i) + "' > iplist  && cat iplistB >> iplist")
  os.system("scp ./iplist " + serverA[i] + ":~/repnet/exp_code/iplist")
  print "Done copying iplist to", serverA[i]
for j in range(1, numB+1):
  os.system("echo '" + str(i+j) + "' > iplist  && cat iplistA >> iplist")
  cmd = "scp ./iplist " + serverB[j] + ":~/repnet/exp_code/iplist"
  os.system(cmd)
  print "Done copying iplist to", serverB[j]

os.system("rm iplist*")
