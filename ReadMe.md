# Dynamic DNS Updater

## Purpose
This repository consists of daemon to update dynu.com dynamic dns with the latest IP address. This is done every 30 minutes and populates both IPv4 and IPv6.

## Install script
1. Run the installation script (may require sudo) `./install.sh`
2. Configure the software by filling out the domain and api key in /etc/dynamic-dns-update.conf


## Install script breakdown
1. copy main.py to /usr/local/bin/dynamic-dns.py
  `cp main.py /usr/local/bin/dynamic-dns`
2. copy dynamic-dns-update.service to /etc/systemd/system/
  `cp dynamic-dns-update.service /etc/systemd/system/`
3. copy dynamic-dns-update.conf.sample to /etc/dynamic-dns-update.conf
  `cp dynamic-dns-update.conf.sample /etc/dynamic-dns-update.conf`
4. chmod +x to the copied files - to allow execution
  `chmod +x /etc/systemd/system/dynamic-dns-update.service`
  `chmod +x /usr/local/bin/dynamic-dns.py`


## References:
- https://tecadmin.net/setup-autorun-python-script-using-systemd/
