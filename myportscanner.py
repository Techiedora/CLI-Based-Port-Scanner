#!/usr/bin/python3

from argparse import ArgumentParser
import socket
from threading import Thread, Lock
from time import time

open_ports = []
lock = Lock()  # To ensure thread-safe access to open_ports

def prepare_args():
    """Prepare arguments."""
    parser = ArgumentParser(description="Python Based Port Scanner", 
                            usage="%(prog)s 192.168.1.2",
                            epilog="Example: %(prog)s -s 20 -e 40000 -t 500 -V 192.168.1.2")
    parser.add_argument(metavar="IPv4", dest="ip", help="host to scan")
    parser.add_argument("-s", "--start", dest="start", metavar="", type=int, help="starting port", default=1)
    parser.add_argument("-e", "--end", dest="end", metavar="", type=int, help="ending port", default=65535)
    parser.add_argument("-t", "--threads", dest="threads", metavar="", type=int, help="threads to use", default=500)
    parser.add_argument("-V", "--verbose", dest="verbose", action="store_true", help="verbose output")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help="display version")
    
    args = parser.parse_args()
    return args

def prepare_ports(start:int, end:int):
    """Prepare a list of ports from start to end."""
    if start > end:
        raise ValueError("Starting port cannot be greater than ending port.")
    return list(range(start, end + 1))  # Convert to list for thread safety

def scan_port(port):
    """Scan a single port."""
    try:
        with socket.socket() as s:  # Ensure socket is closed after use
            s.settimeout(1)  # Consider making this configurable
            s.connect((arguments.ip, port))
            with lock:  # Ensure thread-safe access
                open_ports.append(port)
            if arguments.verbose:
                print(f"Open port found: {port}")
    except (ConnectionRefusedError, socket.timeout, OSError):
        pass

def prepare_threads(threads:int, ports):
    """Create and start threads."""
    thread_list = []
    
    for port in ports:
        thread = Thread(target=scan_port, args=(port,))
        thread_list.append(thread)
        thread.start()
        
        if len(thread_list) >= threads:
            for t in thread_list:
                t.join()  # Wait for all threads to finish
            thread_list = []  # Reset for next batch

    # Join any remaining threads
    for t in thread_list:
        t.join()

if __name__ == "__main__":
    arguments = prepare_args()
    
    try:
        ports = prepare_ports(arguments.start, arguments.end) 
        start_time = time()
        
        prepare_threads(arguments.threads, ports)  
        
        end_time = time()
        
        if arguments.verbose:
            print()

        print(f"Open Ports Found - {open_ports}")
        print(f"Time Taken - {round(end_time - start_time, 2)} seconds")
    
    except ValueError as e:
        print(f"Error: {e}")
