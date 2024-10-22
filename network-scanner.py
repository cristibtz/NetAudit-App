import sys
import scapy.all as scapy
import socket

#Currently only scans internal network
def scan_network(netowrk):

    print()
    print("Sending ARP requests...")

    arp_frame = scapy.ARP(pdst = network)

    broadcast_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")

    broadcast_arp_frame = broadcast_frame / arp_frame

    replies = scapy.srp(broadcast_arp_frame, timeout = 5, verbose = False)[0]

    hosts = []

    for i in range(0, len(replies)):
        ip = replies[i][1].psrc
        mac = replies[i][1].hwsrc
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Unknown"
        host = { 
                "ip": ip,
                "mac": mac.upper(),
                "hostname": hostname
                }
        hosts.append(host)

    return hosts

def display_hosts(hosts):
    no_of_hosts = len(hosts)
    print()
    print(f"There are probably {no_of_hosts} active hosts.")
    print()
    print("------------------------ HOSTS ------------------------")
    print()

    for i in range(0, no_of_hosts):
        print(f"{i}. " + "IP ADDRESS: " + hosts[i]["ip"] + " | " + "MAC ADDRESS: " + hosts[i]["mac"] + " | " + \
              "HOSTNAME: " + hosts[i]["hostname"]
              )
    
    print()
    print("-------------------------------------------------------")

if __name__ == "__main__":

    network = sys.argv[1]

    hosts = scan_network(network)

    display_hosts(hosts)