''' Simple data center controller

    @author Milad Sharif (msharif@stanford.edu)
    
    based on riplpox 
'''

import logging

import sys
sys.path.append('/home/ubuntu/hedera/')

from struct import pack
from zlib import crc32

from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.udp import udp
from pox.lib.packet.tcp import tcp
import pox.lib.packet as pkt

from util import buildTopo, getRouting


log = core.getLogger()

# Number of bytes to send for packet_ins
MISS_SEND_LEN = 2000

class Switch(EventMixin):
    def __init__(self):
        self.connection = None
        self.dpid = None
        self.ports = None

    def connect(self, connection):
        if self.dpid is None:
            self.dpid = connection.dpid
        assert self.dpid == connection.dpid
        self.connection = connection
    
    def send_packet_data(self, outport, data = None):
        msg = of.ofp_packet_out(in_port=of.OFPP_NONE, data = data)
        msg.actions.append(of.ofp_action_output(port = outport))
        self.connection.send(msg)
    
    def send_packet_bufid(self, outport, buffer_id = -1):
        msg = of.ofp_packet_out(in_port=of.OFPP_NONE)
        msg.actions.append(of.ofp_action_output(port = outport)) 
        msg.buffer_id = buffer_id
        self.connection.send(msg)
                        
    def install(self, port, match, modify = False, buf = -1, idle_timeout = 0, hard_timeout = 0):
        msg = of.ofp_flow_mod()
        msg.match = match
        if modify:
            msg.command = of.OFPFC_MODIFY_STRICT
        else: 
            msg.command = of.OFPFC_ADD
        msg.idle_timeout = idle_timeout
        msg.hard_timeout = hard_timeout
        msg.actions.append(of.ofp_action_output(port = port))
        #msg.buffer_id = buf          
        msg.flags = of.OFPFF_SEND_FLOW_REM

        self.connection.send(msg)

    def stat(self, port):
        msg = of.ofp_stats_request()
        # msg.type = of.OFPST_FLOW
        msg.body = of.ofp_flow_stats_request()
        #msg.body.match.in_port = port
        self.connection.send(msg) 
 
class DCController(EventMixin):
    def __init__(self, t, r):
        self.switches = {}  # [dpid]->switch
        self.macTable = {}  # [mac]->(dpid, port)
        self.t = t          # Topo object
        self.r = r          # Routng object
        self.all_switches_up = False
        core.openflow.addListeners(self)
    
    def _ecmp_hash(self, packet):
        ''' Return an ECMP-style 5-tuple hash for TCP/IP packets, otherwise 0.
        RFC2992 '''
        hash_input = [0] * 5
        if isinstance(packet.next, ipv4):
            ip = packet.next
            hash_input[0] = ip.srcip.toUnsigned()
            hash_input[1] = ip.dstip.toUnsigned()
            hash_input[2] = ip.protocol
            if isinstance(ip.next, tcp) or isinstance(ip.next, udp):
                l4 = ip.next
                hash_input[3] = l4.srcport
                hash_input[4] = l4.dstport
                return crc32(pack('LLHHH', *hash_input))
        return 0

    def _flood(self, event):
        ''' Broadcast to every output port '''
        packet = event.parsed
        dpid = event.dpid
        in_port = event.port
        t = self.t 
        # Broadcast to every output port except the input on the input switch.
        for sw_name in t.layer_nodes(t.LAYER_EDGE):
            for host_name in t.lower_nodes(sw_name):
                sw_port, host_port = t.port(sw_name, host_name)
                sw = t.node_gen(name = sw_name).dpid

                # Send packet out each non-input host port
                if sw != dpid or (sw == dpid and in_port != sw_port):
                    self.switches[sw].send_packet_data(sw_port, event.data)


    def _install_reactive_path(self, event, out_dpid, final_out_port, packet):
        ''' Install entries on route between two switches. '''
        in_name = self.t.node_gen(dpid = event.dpid).name_str()
        out_name = self.t.node_gen(dpid = out_dpid).name_str()
        hash_ = self._ecmp_hash(packet)

        # EDIT: if ICMP (ping), then routed to a fixed destination
        if packet.payload.protocol == pkt.ICMP_PROTOCOL:
            ip = packet.next
            pingrank = (ip.srcip.toUnsigned()) % 6
            route = self.r.get_route(in_name, out_name, pingrank)
        else:
            route = self.r.get_route(in_name, out_name, hash_) 
        if route is None:
            return

        match = of.ofp_match.from_packet(packet)
        for i, node in enumerate(route):
            node_dpid = self.t.node_gen(name = node).dpid
            if i < len(route) - 1:
                next_node = route[i + 1]
                out_port, next_in_port = self.t.port(node, next_node)
            else:
                out_port = final_out_port
            self.switches[node_dpid].install(out_port, match, idle_timeout = 10)
        
    def _handle_FlowStatsReceived (self, event):
        pass

    def _handle_PacketIn(self, event):
        if not self.all_switches_up:
            log.debug("Saw PacketIn before all switches were up - ignoring." )
            return
        
        packet = event.parsed
        dpid = event.dpid
        in_port = event.port

        # Learn MAC address of the sender on every packet-in.
        self.macTable[packet.src] = (dpid, in_port)

    
        # Insert flow, deliver packet directly to destination.
        if packet.dst in self.macTable:
            out_dpid, out_port = self.macTable[packet.dst]
            self._install_reactive_path(event, out_dpid, out_port, packet)
        
            self.switches[out_dpid].send_packet_data(out_port, event.data)
            
        else:
            self._flood(event)

    def _handle_ConnectionUp(self, event):
        sw = self.switches.get(event.dpid)
        sw_str = dpidToStr(event.dpid)
        sw_name = self.t.node_gen(dpid = event.dpid).name_str()
        
        if sw_name not in self.t.switches():
            log.warn("Ignoring unknown switch %s" % sw_str)
            return

        if sw is None:
            log.info("Added a new switch %s" % sw_name)
            sw = Switch()
            self.switches[event.dpid] = sw
            sw.connect(event.connection)
        else:
            log.debug("Odd - already saw switch %s come up" % sw_str)
            sw.connect(event.connection)

        sw.connection.send(of.ofp_set_config(miss_send_len=MISS_SEND_LEN))

        if len(self.switches)==len(self.t.switches()):
            log.info("All of the switches are up")
            self.all_switches_up = True

def launch(topo = None, routing = None):
    if not topo:
        raise Exception ("Please specify the topology")
    else: 
        t = buildTopo(topo)
    r = getRouting(routing, t)

    core.registerNew(DCController, t, r)
    log.info("*** Controller is running")

