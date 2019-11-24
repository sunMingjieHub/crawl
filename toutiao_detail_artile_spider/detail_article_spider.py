import telnetlib
import json
import random
from multiprocessing.pool import Pool
import multiprocessing
from selenium import webdriver
import time
import threading
from selenium.common.exceptions import NoSuchElementException

proxy_lock = threading.Lock()
proxy = {}
ips = []
mark = 0
mark_lock = threading.Lock()


def get_proxy():
    global proxy
    global ips
    while True:
        proxy_lock.acquire()
        f = open('verified_proxies.json', 'r+')
        for line in f:
            jd = json.loads(line)
            ips.append(jd)
        try:
            proxy = random.choice(ips)
        finally:
            proxy_lock.release()
        time.sleep(300)


def get_urls():
    global mark
    global mark_lock
    with open("mark_locate.csv") as csvfile:
        mLines = csvfile.readlines()
    targetLine = mLines[-1]

    mark_lock.acquire()
    try:
        mark = int( targetLine.split(',')[0])
    finally:
        mark_lock.release()
    i =0
    ids=[]
    with open('toutiao_cat_data.txt','r+') as fp:
        for lines in fp:
            i=i+1
            if i<mark:
                continue
            temp = lines.split('_!_')
            article_id = temp[0]
            code = temp[1]
            them =temp[2]
            title = temp[3]
            title="".join(title.split('/'))
            ids.append({'article_id':article_id,'theme':them,'code':code,'title':title})
    return ids


def get_articles(a_id):
    global content
    global mark_lock
    global mark
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.set_preference('permissions.default.image', 2)
    profile = set_profile()
    seleiun = Myselenium(options, profile)
    time.sleep(1)
    #print(a_id)
    detail_url = 'https://www.toutiao.com/a' + str(a_id['article_id'])
    print(detail_url)
    browser = seleiun.get_browser()
    browser.get(detail_url)
    browser.implicitly_wait(5)
    time.sleep(1)
    content = ""
    for i in range(2):
        js = "var q=document.documentElement.scrollTop=(Math.ceil(Math.random()*10000)); "
        browser.execute_script(js)
        time.sleep(1)
    if seleiun.is_element_present('//div[@class="article-content"]'):
        # print('content')
        content = browser.find_element_by_xpath('//div[@class="article-content"]').text
    elif seleiun.is_element_present('//div[@class="a-con"]'):
        # print('a-con')
        content = browser.find_element_by_xpath('//div[@class="a-con"]').text
    elif seleiun.is_element_present('//div[@class="answers"]'):
        # print('answer')
        contents = browser.find_elements_by_xpath('//div[@class="answer-text-full rich-text"]')
        content = ""
        for c in contents:
            content = content + c.text
        # print(ss)
    else:
        try:
            content = browser.find_element_by_xpath('//article').text
            # print('//article')
        except:
            # print("NoElementException:", browser.current_url)
            content = ""
            pass
    browser.quit()
    # print(a_id[0],a_id[3])
    title = "toutiao_article/" + a_id['article_id'] + "" + a_id['title'] + ".txt"
    title = "".join(title.split(' '))
    # print(title)
    with open(title, 'w') as fp:
        fp.write(content)
    mark_lock.acquire()
    try:
        with open('mark_locate.csv', 'a+') as f2:
            mark = mark + 4
            f2.write('\n')
            f2.write(str(mark))
    finally:
        mark_lock.release()


class Myselenium(object):
    def __init__(self, options, profile):
        self._browser = webdriver.Firefox(options=options, firefox_profile=profile)

    def get_browser(self):
        return self._browser

    def is_element_present(self, value):

        """
        用来判断元素标签是否存在，
        """
        try:
            # print(driver.page_source)
            element = self._browser.find_element_by_xpath(value)
        # print(value)
        # 原文是except NoSuchElementException, e:
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True


def set_profile():
    global proxy
    while True:
        try:
            telnetlib.Telnet(proxy['host'], port=proxy['port'], timeout=3)
        except:
            proxy_lock.acquire()
            try:
                proxy = random.choice(ips)
            finally:
                proxy_lock.release()
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


if __name__ == '__main__':
    ids = get_urls()
    th = threading.Thread(target=get_proxy)
    th.start()
    time.sleep(2)
    pool = Pool(processes=4)
    pool.map(get_articles,ids)





