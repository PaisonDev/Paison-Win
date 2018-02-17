import os
import ipgetter
myip = ipgetter.myip()
while True:
  os.system("wget http://%s/url.php")
  os.system("rm -rf url.php.*")
