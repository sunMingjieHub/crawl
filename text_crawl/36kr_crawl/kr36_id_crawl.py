import json
import telnetlib

from selenium import webdriver
from lxml import etree
import time
from multiprocessing import Pool
import random
root_utl = "https://36kr.com"
proxy = {}
crwal_urls = [
    'contact/',
    'travel/',
    'technology/',
    'enterpriseservice/',
    'happy_life/',
    'web_zhichang/',
    'innovate/',
]
browser1 = webdriver.Firefox()
ips=[]


def set_profile():
    global proxy
    while True:
        try:
            telnetlib.Telnet(proxy['host'], port=proxy['port'], timeout=3)
            print(",",proxy)
        except:
            proxy = random.choice(ips)
            print("]",proxy)
            continue
        else:
            break

    proxy_host = proxy['host']
    type = proxy['type']
    proxy_port = proxy['port']
    profile = webdriver.FirefoxProfile()
    ## 第二步：开启“手动设置代理”
    profile.set_preference('network.proxy.type', 1)
    ## 第三步：设置代理IP
    if type == 'http':
        profile.set_preference('network.proxy.http', proxy_host)
        ## 第四步：设置代理端口，注意端口是int类型，不是字符串
        profile.set_preference('network.proxy.http_port', proxy_host)
    else:
        profile.set_preference('network.proxy.ssl', proxy_host)
        profile.set_preference('network.proxy.ssl_port', proxy_port)
    print(proxy)
    return profile


lastl =0
nowl =0


def get_proxy():
    global proxy
    global ips
    f = open('verified_proxies.json', 'r+')
    for line in f:
        jd = json.loads(line)
        ips.append(jd)
        proxy = random.choice(ips)
    f.close()


def get_urls(theme,isfirst):
    global browser1
    browser1.get(root_utl + '/information/' + theme)
    browser1.implicitly_wait(5)
    count =0
    for i in range(300):
        print("i",i)
        for j in range(random.randint(2,3)):
            js = f"var q=document.documentElement.scrollTop={random.randint(300, 8000)}"
            browser1.execute_script(js)
            time.sleep(1)
        try:
            browser1.find_element_by_xpath('//div[@class="kr-loading-more-button show"]').click()
            time.sleep(1)
        except Exception as e:
            print(e)
            count =count+1
            print("count",count)
            if count>5:
                break
    web = etree.HTML(browser1.page_source)
    try:
        items = web.xpath('//div[@class="information-flow-item"]')
        print(len(items))
        if len(items) > 0:
            item_id_urls = items[0].xpath('//a[contains(@class,"article-item-title")]/@href')
            print(item_id_urls)
            with open("kr36_id.txt",'a+') as fp:
                for item_id in item_id_urls:
                    fp.write(item_id+"_"+theme)
                    fp.write('\n')

                # detail_url = root_utl + item_id
                # get_article(detail_url, theme)
                # time.sleep(2)

    except Exception as e:
        print("get_urls",e)


# def next_page(theme):
#     global browser1
#     try:
#         browser1.find_element_by_xpath('//div[@class="kr-loading-more-button show"]').click()
#         time.sleep(3)
#         get_urls(theme=theme,isfirst=False)
#     except Exception as e:
#         print("next_page",e)
#         print(browser1.page_source)
#         return


def get_article(url,theme):
    global browser2
    browser2.get(url)
    browser2.implicitly_wait(10)
    title = browser2.find_element_by_xpath('//h1[contains(@class,"article-title" )]').text
    content = browser2.find_element_by_xpath('//div[contains(@class,"articleDetailContent")]').text
    title = "kr36_article/"+title+".txt"
    #print(title)
    with open(title,"w") as fp:
        fp.write(theme)
        fp.write('\n')
        fp.write(content)
    fp.close()


def set_driver():
    global browser1
    global browser2
    profile1 = set_profile()
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference('permissions.default.image', 2)
    options1 = webdriver.FirefoxOptions()
    options1.add_argument('-headless')
    browser1 = webdriver.Firefox(options=options, firefox_profile=profile1)
    browser2 = webdriver.Firefox(options=options1)


if __name__ == '__main__':
    get_proxy()
    time.sleep(2)
    set_driver()
    for themeurl in crwal_urls:
        print(themeurl)
        get_urls(themeurl, True)