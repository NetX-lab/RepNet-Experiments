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

    for i in range(0, hnum):
        h[i].cmd("python ~/mininet-repnet/run_time_load_id.py " + runtime + " " + load + " " + str(i) + " &")

    h[3].cmd("ping -c10000 -i0.1 10.5.1.2 > ping2.trace & ")
    h[4].cmd("ping -c10000 -i0.1 10.5.1.3 > ping3.trace & ")
    h[5].cmd("ping -c10000 -i0.1 10.5.1.4 > ping4.trace ")

    time.sleep(3)
    net.stop()
