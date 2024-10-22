import sys
import scapy.all as scapy

network = sys.argv[1]

arp_frame = scapy.ARP(pdst = network)

broadcast_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")

broadcast_arp_frame = broadcast_arp_frame / arp_frame

replies = arp_frame.srp(broadcast_arp_frame, timeout = 1, verbose = False)[0]

print(replies)