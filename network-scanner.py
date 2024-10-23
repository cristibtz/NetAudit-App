import scapy.all as scapy
from queue import Queue
import sys, socket, ipaddress, threading, time

#Currently only scans internal network

print()
print("Sending ARP requests...")
print("Found hosts:")
print()

hosts = []
queue = Queue()

def check_host():
    while not queue.empty():

        ip = queue.get()    

        arp_frame = scapy.ARP(pdst = ip)

        broadcast_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")

        broadcast_arp_frame = broadcast_frame / arp_frame

        reply = scapy.srp1(broadcast_arp_frame, timeout = 5, verbose = False)

        if reply:

            mac = reply.hwsrc
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
            print("-- " + "IP ADDRESS: " + host["ip"] + " | " + "MAC ADDRESS: " + host["mac"] + " | " + \
              "HOSTNAME: " + host["hostname"] + " --"
              )
        queue.task_done()

def display_hosts(hosts):
    no_of_hosts = len(hosts)
    if no_of_hosts == 0:
        print("No hosts found.")
        exit()
    
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
    print()

if __name__ == "__main__":
    network = sys.argv[1]
    ip_list = [str(ip) for ip in ipaddress.IPv4Network(network, strict=False)]

    for ip in ip_list:
        queue.put(ip)

    num_threads = 50
    threads = []
    
    try:
        for _ in range(num_threads):
            thread = threading.Thread(target = check_host)
            thread.daemon = True
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(1)
    except KeyboardInterrupt:
        print("Exiting...")        
          
    
    print()
    print("SCAN COMPLETE!")
    display_hosts(hosts)

