 sudo cp main.py /usr/local/bin/dynamic-dns.py
 sudo cp dynamic-dns-update.service /etc/systemd/system/
 sudo cp dynamic-dns-update.conf.sample /etc/dynamic-dns-update.conf
 sudo chmod +x /etc/systemd/system/dynamic-dns-update.service
 sudo chmod +x /usr/local/bin/dynamic-dns.py
