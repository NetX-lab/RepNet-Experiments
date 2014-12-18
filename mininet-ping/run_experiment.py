from dctopo import FatTreeTopo #, VL2Topo, TreeTopo
import sys
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

if __name__ == '__main__':
    runtime = sys.argv[1]
    load = sys.argv[2]
    setLogLevel('info')
    fattree = FatTreeTopo(k=6, speed=0.02)
    net = Mininet(topo=fattree, link=TCLink, controller=RemoteController)
    net.start()
    h = net.hosts
    hnum = len(h)
    time.sleep(5)

    for i in range(0, hnum - 1):
        h[i].cmd("python ~/mininet-repnet/run_time_load_id.py " + runtime + " " + load + " " + str(i) + " &")
    h[hnum-1].cmdPrint("python ~/mininet-repnet/run_time_load_id.py " + runtime + " " + load + " " + str(hnum-1))

    time.sleep(3)
    net.stop()
