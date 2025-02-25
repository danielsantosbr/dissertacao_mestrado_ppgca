from scapy.all import *

# Load the PCAP file
pkts = rdpcap("gen_man_udp_tcp_ftp_http_get_1M.pcap")

# Loop through each packet in the PCAP file
for i, pkt in enumerate(pkts):
    # Create the new MAC address
    new_mac = "00:00:00:00:00:%02d" % (i + 1)
    # Change the source and destination MAC addresses
    pkt[Ether].src = new_mac
    pkt[Ether].dst = new_mac
    # change IPs
    pkt[IP].src = "10.0.0.%d" % (i + 1)
    pkt[IP].dst = "10.0.0.%d" % (i + 1)

# Write the modified packets to a new PCAP file
wrpcap("gen_man_udp_tcp_ftp_http_get_1M_mod.pcap", pkts)