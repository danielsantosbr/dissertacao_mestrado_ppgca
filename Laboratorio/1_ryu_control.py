from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, in_proto, ipv4, icmp, tcp, udp

class CustomSDNController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(CustomSDNController, self).__init__(*args, **kwargs)
        self.mac_port_mapping = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def handle_switch_features(self, event):
        dp = event.msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        # Configura a entrada de fluxo padrão (table-miss)
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        self.install_flow(dp, 0, match, actions)

    def install_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofp = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            flow_mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                         priority=priority, match=match,
                                         instructions=instructions)
        else:
            flow_mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                         match=match, instructions=instructions)
        datapath.send_msg(flow_mod)

    def send_packet(self, msg, actions):
        dp = msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser
        in_port = msg.match['in_port']

        data = msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None
        packet_out = parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                                         in_port=in_port, actions=actions, data=data)
        dp.send_msg(packet_out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def handle_packet_in(self, event):
        msg = event.msg
        dp = msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return  # Ignora pacotes LLDP

        src_mac = eth.src
        dst_mac = eth.dst
        dpid = dp.id
        self.mac_port_mapping.setdefault(dpid, {})

        self.logger.info("Pacote recebido: DPID=%s, MAC de origem=%s, MAC de destino=%s, Porta de entrada=%s",
                         dpid, src_mac, dst_mac, in_port)

        self.mac_port_mapping[dpid][src_mac] = in_port

        out_port = self.mac_port_mapping[dpid].get(dst_mac, ofp.OFPP_FLOOD)
        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofp.OFPP_FLOOD and eth.ethertype == ether_types.ETH_TYPE_IP:
            ip_pkt = pkt.get_protocol(ipv4.ipv4)
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst
            protocol = ip_pkt.proto

            if protocol == in_proto.IPPROTO_ICMP:
                match = parser.OFPMatch(
                    eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src=src_ip,
                    ipv4_dst=dst_ip,
                    eth_src=src_mac,
                    eth_dst=dst_mac,
                    in_port=in_port,
                    ip_proto=protocol
                )
            elif protocol == in_proto.IPPROTO_UDP:
                udp_pkt = pkt.get_protocol(udp.udp)
                match = parser.OFPMatch(
                    eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src=src_ip,
                    ipv4_dst=dst_ip,
                    eth_src=src_mac,
                    eth_dst=dst_mac,
                    ip_proto=protocol,
                    in_port=in_port,
                    udp_src=udp_pkt.src_port,
                    udp_dst=udp_pkt.dst_port
                )
            elif protocol == in_proto.IPPROTO_TCP:
                tcp_pkt = pkt.get_protocol(tcp.tcp)
                match = parser.OFPMatch(
                    eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src=src_ip,
                    ipv4_dst=dst_ip,
                    eth_src=src_mac,
                    eth_dst=dst_mac,
                    ip_proto=protocol,
                    in_port=in_port,
                    tcp_src=tcp_pkt.src_port,
                    tcp_dst=tcp_pkt.dst_port
                )

            if msg.buffer_id != ofp.OFP_NO_BUFFER:
                self.install_flow(dp, 1, match, actions, msg.buffer_id)
                return
            else:
                self.install_flow(dp, 1, match, actions)

        data = msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None
        packet_out = parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                                         in_port=in_port, actions=actions, data=data)
        dp.send_msg(packet_out)