from pox.core import core
from pox.lib.util import dpidToStr
from pox.lib.revent import EventHalt
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class DijkstraController(object):
    def __init__(self):
        core.openflow.addListeners(self)
        log.info("DijkstraController initialized")

    def _handle_ConnectionUp(self, event):
        log.info("Switch connected: %s", dpidToStr(event.dpid))

    def _handle_ConnectionDown(self, event):
        log.info("Switch disconnected: %s", dpidToStr(event.dpid))

    def _handle_PacketIn(self, event):
        packet = event.parsed
        log.info("PacketIn received on switch %s: %s", dpidToStr(event.dpid), packet)
        
        # Flood the packet to all ports except the incoming port
        self.flood_packet(event, packet)

    def flood_packet(self, event, packet):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        raise EventHalt

def launch():
    core.registerNew(DijkstraController)

