# utility functions

from DCTopo import FatTreeTopo
from mininet.util import makeNumeric
from DCRouting import HashedRouting

TOPOS = {'ft': FatTreeTopo}
ROUTING = {'ECMP' : HashedRouting}


def buildTopo(topo):
    topo_name, topo_param = topo.split( ',' )
    return TOPOS[topo_name](makeNumeric(topo_param))


def getRouting(routing, topo):
    return ROUTING[routing](topo)
