#!/bin/bash

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
        yum install MySQL-python
        pip install parallel-ssh


elif [ $(echo $DISTRO | grep -i "Debian" | wc -l) -eq 1 ]; then
        apt-get install php libapache2-mod-php php-mcrypt php-mysql -y
        apt-get install apache2 -y 
        apt-get install python gcc screen -y
        sudo service apache2 restart
        apt-get install python-setuptools -y 
        apt-get install python-pip -y 
        apt-get install MySQL-python -y
        pip install parallel-ssh

elif [ $(echo $DISTRO | grep -i "Ubuntu" | wc -l) -eq 1 ]; then
        apt-get install php libapache2-mod-php php-mcrypt php-mysql -y
        apt-get install apache2 -y 
        apt-get install python gcc screen -y
        sudo service apache2 restart 
        apt-get install python-setuptools -y 
        apt-get install python-pip -y
        apt-get install MySQL-python -y
        pip install parallel-ssh
        
else
        echo "Unknown OS"
fi

echo "Making Directories"

mkdir /var/log/Paison
mkdir /var/log/Paison/Logs
mkdir /var/log/Paison/Accounts

echo "Making Files"
touch /var/log/Paison/ssh_servers.txt
touch /var/log/Paison/banner.txt
touch /var/log/Paison/Logs/device_feedback.log


