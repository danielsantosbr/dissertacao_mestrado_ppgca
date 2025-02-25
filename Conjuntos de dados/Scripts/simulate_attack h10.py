from scapy.all import *

# Read packets from .pcap file
packets = rdpcap("/mnt/NVME_500/DS/DARPA 2009/mypcap_20091105075102.pcap")

# Send packets to Mininet network
for packet in packets:
    packet.show()
    sendp(packet, iface="h10-eth0")
