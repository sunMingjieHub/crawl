import json
import telnetlib
import requests
import time


proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'


def verify(ip,port,type):
    proxies = {}
    try:
        telnet = telnetlib.Telnet(ip,port=port,timeout=3)
    except:
        print('unconnected')
    else:
        #print('connected successfully')
        # proxyList.append((ip + ':' + str(port),type))
        proxies['type'] = type
        proxies['host'] = ip
        proxies['port'] = port
        proxiesJson = json.dumps(proxies)
        with open('verified_proxies.json','a+') as f:
            f.write(proxiesJson + '\n')
        f.close()
        print("已写入：%s" % proxies)


def get_proxy(proxy_url):
    response = requests.get(proxy_url)
    proxies_list = response.text.split('\n')
    for proxy_str in proxies_list:
        proxy_json = json.loads(proxy_str)
        host = proxy_json['host']
        port = proxy_json['port']
        type = proxy_json['type']
        if type == 'http':
            verify(host,port,type)


if __name__ == '__main__':
    while True:
        get_proxy(proxy_url)
        time.sleep(1800)
