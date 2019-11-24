import requests
url = 'http://icanhazip.com'
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
proxy = {
    "http":"216.189.145.240:80",
}
#
# response = requests.get(url,proxies=proxy)
# print(response.text)
profile = webdriver.FirefoxProfile()
options = webdriver.FirefoxOptions()

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "159.138.3.119:80"
# prox.ssl_proxy = "159.203.87.130:3128"


browser = webdriver.Firefox(options=options, firefox_profile=profile)
# proxy1 = {"type": "https", "host": "185.75.5.158", "port": 60819}
#
browser.firefox_profile.set_preference('network.proxy.http', '216.189.145.240')
## 第四步：设置代理端口，注意端口是int类型，不是字符串
browser.firefox_profile.set_preference('network.proxy.http_port', 80)
# browser.firefox_profile.set_proxy(prox)
# browser.profile.set_proxy(prox)
browser.get(url)
print(browser.page_source)
