import requests
import re
import time

cur_ip = None
DOMAIN = 'raspwebserver.duckdns.org'
TOKEN = 'ec7e753c-62c1-4a7f-aa28-dc5b032d80c3'
UPDATE_INTERVAL = 10 # in seconds

def send_dns_update_req():
    global cur_ip, DOMAIN, TOKEN
    httpr = None
    while True:
        params = {'domains': DOMAIN, 'token': TOKEN, 'ip': cur_ip, 'verbose': 'true'}
        httpr = requests.get('https://www.duckdns.org/update', params=params)
        res = httpr.text.split('\n')[0]
        if res == 'OK':
            break
        else:
            print('Resending update dns request')

def get_cur_ip():
    httpr = requests.get('https://ip4only.me/api/')
    new_ip = re.findall(r'((?:\d+\.){3}\d+)', httpr.text)[0]
    return new_ip

def main():
    global cur_ip, UPDATE_INTERVAL
    while True:
        new_ip = get_cur_ip()
        if cur_ip is None or cur_ip != new_ip:
            cur_ip = new_ip
            send_dns_update_req()
            # print(f'CHANGED -> NEW-IP = {cur_ip}')
            print('CHANGED -> NEW-IP = ' + str(cur_ip))
        else:
            # print(f'NO CHANGE -> CUR-IP = {cur_ip}')
            print('NO CHANGE -> CUR-IP = ' + str(cur_ip))
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    main()