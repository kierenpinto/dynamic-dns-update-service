# Dynamic DNS Updater

## Install instructions
- Step 1 copy main.py to /usr/local/bin/dynamic-dns.py
  `cp main.py /usr/local/bin/dynamic-dns`
- Step 2 copy dyanmic-dns-update.service to /etc/systemd/system/
  `cp dynamic-dns-update.service /etc/systemd/system/`
- Step 3 chmod +x to the copied files - to allow execution
  `chmod +x /etc/systemd/system/dyanmic-dns-update.service`
  `chmod +x /usr/local/bin/dynamic-dns.py`


### Install script
The above steps are in install.sh
