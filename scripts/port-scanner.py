from queue import Queue
import socket, threading, sys
import argparse

parser = argparse.ArgumentParser(description="Web Fuzzer", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--host", required=True, help="IP address to scan")
parser.add_argument("-t", "--threads", required=True, help="Number of threads to use")
parser.add_argument("-m", "--mode", required=True, help="Mode of scan: 1 for well-known ports, 2 for all ports, 3 for popular service ports")


queue = Queue()
open_ports = []

def portscan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except: 
        return False


def get_ports(mode):

    #Mode for well-known ports
    if mode == 1:

        for port in range(1, 1024):
            queue.put(port)

    #Mode for all ports
    elif mode == 2:

        for port in range(1, 65535):
            queue.put(port)

    #Mode for popular service ports
    elif mode == 3:

        ports = [20, 21, 22,23 ,25 ,53 ,80 ,110 ,443, 445]

        for port in ports:
            queue.put(port)

def scanner(target):

    while not queue.empty():
        port = queue.get()
        if portscan(target, port):

            print("Port {} is open!".format(port))

            open_ports.append(port)
        
def run_scanner(target, threads, mode):

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target = scanner, kwargs={"target": target}) 
        thread.daemon = True
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join(1)

    print("Scan completed!")

    return open_ports

if __name__ == "__main__":
        
        args = parser.parse_args()
        
        target = args.host
        threads_no = args.threads
        mode = args.mode

        print("Starting scan on target: " + target)
        print("-" * 64)
        ports = run_scanner(target, int(threads_no), int(mode))  

        if ports != []:
            print("Found " +  f"{len(ports)} " + " open ports: ")
            for port in ports:
                print(port)
        else:
            print("No open ports found")

