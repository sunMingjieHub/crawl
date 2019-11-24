# -*-coding:utf8-*-

import requests
from lxml import etree
import time


hearders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

url = 'http://society.people.com.cn/n1/2019/1115/c1008-31458083.html'
'/html/body/div[5]/h1'


def get_info():
    web = requests.get(url,hearders)
    html = web.text.encode('latin1').decode("GBK")
    selector = etree.HTML(html)
    title = selector.xpath('//div[contains(@class,"text_title")]/h1/text()')[0]
    print(title)
    data = selector.xpath('//div[@id = "rwb_zw"]')[0]
    content = data.xpath('string(.)')
    print(content)
    title = title+".txt"
    fp= open(title,"w")
    fp.write(content)
    fp.close()


if __name__ == '__main__':
    urls = [
        'http://society.people.com.cn/GB/136657/index4.html'
    ]
    get_info()