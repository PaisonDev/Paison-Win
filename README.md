# PaisonBot Linux Development
PaisonBot has no intent to be malicious, or classed as malware.

## Python Requirements
python-setuptools python-pip ipgetter parallel-ssh requests

## Linux Requirements
gcc screen php php-mysql php-devel php-gd php-pecl-memcache php-pspell php-snmp php-xmlrpc php-xml httpd/apache2

## Network Requirements
*None*


## Installation
Download / Clone Source, Unzip the File.

-- apt/yum install unzip -y; unzip master.zip

Change your current directory after unzipping.

-- cd Paison-Win-master/

Run Setup.sh

-- chmod +x setup.sh; ./setup.sh

__NOTE__: To change default password: nano/vi into Paison-Win-master/setup.sh, and change the text insde line > 58

Woallah! You're Parallel SSH CNC Server is now setup


## How do I connect?!
Either use putty, Or wait until the custom client is posted.


## Commands
*-help*
    -- Shows All Commands (With Arguments)
    
## How Do I Get Servers?!
nano/vi into the ssh_servers file
    -- nano /var/log/Paison/ssh_servers.txt

Add a new line for every ssh server.
__NOTE__: passwd every ssh server to a static password.

