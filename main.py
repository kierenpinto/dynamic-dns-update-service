from requests import get, post
import time
import json
import ipaddress
import sys
import logging
import os
import configparser

def get_ip():
    ipv4 = get('https://api.ipify.org').text
    ip_universal = get('https://api64.ipify.org').text
    if type(ipaddress.ip_address(ip_universal)) is ipaddress.IPv6Address:
        ipv6 = ip_universal
    else:
        ipv6 = None
    logger.debug("Get IP: "+ str((ipv4, ipv6)))
    return (ipv4, ipv6)

def get_root(domain):
    url = "https://api.dynu.com/v2/dns/getroot/{}".format(domain)

    payload={}
    headers = {
      'API-Key': api_key
    }

    response = get(url, headers=headers, data=payload)
    response.raise_for_status()
    logger.debug("Get DNS Root:"+ response.text)
    return response.json()

def get_dns_record(id):
    url = "https://api.dynu.com/v2/dns/{}".format(id)
    headers = {
      'API-Key': api_key
    }
    response = get(url, headers=headers)
    response.raise_for_status()
    logger.debug("Get DNS Record: "+ response.text)
    return response.json()

def update_dns_record(id, payload):
    url = "https://api.dynu.com/v2/dns/{}".format(id)
    headers = {
      'API-Key': api_key
    }
    response = post(url, headers=headers, data=payload)
    response.raise_for_status()
    log = "Update DNS Request: {}, Response: {}".format(payload, response.text)
    logger.debug(log)
    return response.json()

def update_dns_ip(domain_id, ipv4, ipv6):
    new_payload = {
      "name": domain,
      "ipv4Address": ipv4,
      "ipv6Address": ipv6,
      "ttl": 90,
      "ipv4": True,
      "ipv6": True,
      "ipv4WildcardAlias": True,
      "ipv6WildcardAlias": True,
      "allowZoneTransfer": False,
      "dnssec": False
    }
    json_payload = json.dumps(new_payload)
    return update_dns_record(domain_id, json.dumps(new_payload))

def main(poll_freq):
    logger.info("Start Dynamic DNS Update Process")
    while True:
        try:
            ipv4, ipv6 = get_ip()
            domain_id = get_root(domain)['id']
            update_dns_ip(domain_id, ipv4, ipv6)
            logger.info("Update operation succeeded: {}, {}".format(ipv4,ipv6))
            time.sleep(poll_freq)
        except KeyboardInterrupt:
            logger.info("Stop Dynamic DNS Update Process")
            sys.exit(0)
        except Exception as e:
            logger.error(e)

if __name__ == "__main__":
    global logger
    global domain
    global api_key
    logger = logging.getLogger("DNS Updater")
    logger.setLevel(logging.DEBUG)
    log_dir = os.environ.get('LOG_DIR', './')
    config_dir = os.environ.get('CONF_DIR', './')
    poll_freq = os.environ.get('POLL_FREQ', 60*30)
    config = configparser.ConfigParser()
    config.read(config_dir + 'dynamic-dns-update.conf')
    if config['DEFAULT']:
        api_key = config['DEFAULT']['ApiKey'] if config['DEFAULT']['ApiKey'] else ''
        domain = config['DEFAULT']['Domain'] if config['DEFAULT']['Domain'] else ''
    fh = logging.FileHandler(filename=log_dir+'dynamic_dns_debug.log', mode='a', encoding='utf-8')
    fh_info = logging.FileHandler(filename=log_dir+'dynamic_dns_info.log', mode='a', encoding='utf-8')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    fh_info.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    fh_info.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.addHandler(fh_info)
    main(poll_freq)
