import os
import ipgetter
ip = ipgetter.myip()
url = sys.argv[1]
while True:
  os.system("wget http://%s/url.php?url=%s" % (ip, url)
  os.system("rm -rf url.php.*")
