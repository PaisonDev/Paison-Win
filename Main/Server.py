#!/usr/bin/python
"""
    Author - Aex- (Z)
    Credits - None
"""

import os
import sys
import socket
import getpass
import threading
from pssh.pssh2_client import ParallelSSHClient

user = getpass.getuser()

syntax_prefix = "*"

class puts:

    @staticmethod
    def err(string):
        sys.stderr.write("\033[31m" + string + "\n")

    @staticmethod
    def out(string):
        sys.stdout.write("\033[0m" + string + "\n")


def client():
    pass


def server():
    sock = socket.socket()

    try:
        sock.bind(("127.0.0.1", 3332))
    except socket.error:
        puts.out("[-] Socket Error: Failed to bind to address, Address already in use.")

    sock.listen(0)
    while True: # creating infinite while loop to run forever until error
        try:
            conn, addr = sock.accept()
            puts.out("[+] Connection Recieved. Forwarding client to shell. {}:{}".format(addr[0], addr[1]))
            try:
                threading.Thread(target=client, args=(conn, addr)).start()
            except Exception:
                puts.out("     - could not send client. error occured.")
            
            puts.out("     - sent client to shell.\n")
            

        except socket.error as e:
            puts("[-] Socket Error: Unknown error occured\n%s" + str(e))
