from queue import Queue
import socket, threading, sys

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
        
        target = sys.argv[1]
        threads_no = sys.argv[2]
        mode = sys.argv[3]

        ports = run_scanner(target, int(threads_no), int(mode))  

        if ports != []:
            print("Found " +  f"{len(ports)} " + " open ports: ")
            for port in ports:
                print(port)
        else:
            print("No open ports found")

