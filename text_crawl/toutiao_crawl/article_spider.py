from selenium import webdriver
from bs4 import BeautifulSoup
import re
from lxml import etree
import time
import random

root_utl = "https://www.toutiao.com"
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
options1 = webdriver.FirefoxOptions()
options1.add_argument('-headless')
browser1 = webdriver.Firefox(options=options)
browser2 = webdriver.Firefox(options=options1)

themes = [
    'news_travel/',
    'news_food/',
    'news_tech/',
    'news_game/',
    'news_entertainment/',
    'news_sports/',
    'news_finance/',
    'news_military/',
    'news_history/',
]
lastl = 0
nowl = 0
untitle = 0


def get_article(url_new, theme):
    global untitle
    global browser2
    browser2.get(url_new)
    browser2.implicitly_wait(10)
    time.sleep(10)
    # print(browser.page_source)
    try:
        try:
            content = browser2.find_element_by_xpath(
                '//div[contains(@class,"article-content") or contains(@class,"a-con")]').text
        except:
            content = browser2.find_element_by_xpath('//article').text

        try:
            title = browser2.find_element_by_xpath(
                '//h1[contains(@class,"a-title") or contains(@class,"article-title")]').text
        except Exception as e:
            untitle = untitle + 1
            title = "无标题" + str(untitle)
        title = "toutiao_article/" + title + ".txt"
        with open(title, "w") as fp:
            fp.write(theme)
            fp.write('\n')
            fp.write(content)
        fp.close()
    except Exception as e:
        print("get_article", url_new, theme, e)


def next_page(theme):
    global browser1
    # browser1.execute_script("window.scrollBy(0,3000)")
    # time.sleep(1)
    # browser1.execute_script("window.scrollBy(0,5000)")
    # time.sleep(1)
    # browser1.execute_script("window.scrollBy(0,8000)")
    # time.sleep(1)
    # 将滚动条移动到页面的底部
    # js = "var q=document.documentElement.scrollTop=100000"
    # browser1.execute_script(js)
    # time.sleep(5)
    # # 将滚动条移动到页面的顶部
    # js = "var q=document.documentElement.scrollTop=0"
    # browser1.execute_script(js)
    # time.sleep(5)
    # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
    for i in range(3):
        js = f"var q=document.documentElement.scrollTop={random.randint(10000, 30000)}"
        browser1.execute_script(js)
    time.sleep(5)

    print("scroll")
    # print(browser1.page_source)
    get_url(theme, isFirst=False)


def get_url(theme, isFirst):
    global lastl
    global nowl
    global browser1
    if isFirst:
        browser1.get(root_utl + "/ch/" + theme)
        browser1.implicitly_wait(30)
        time.sleep(5)



    soup = BeautifulSoup(browser1.page_source, "html.parser")
    data = soup.find_all("script")
    for d in data:
        info = re.findall(" var _data = (.*?);", str(d), re.S)
        if len(info) != 0:
            titles = re.findall('"open_url":"(.*?)"', info[0], re.S)

    open_urls = []
    print(len(titles))
    for turl in titles:
        open_urls.append(turl[9:][:-2])
    print(open_urls)
    real_urls = []
    if isFirst:
        lastl = len(open_urls)
        real_urls = open_urls
    else:
        nowl = len(open_urls)
        real_urls = open_urls[lastl:]
        lastl = nowl
    # for ul in real_urls:
    #     ul = 'https://www.toutiao.com/group/'+ul
    #     get_article(ul,theme)
    #     time.sleep(3)
    next_page(theme)


if __name__ == '__main__':
    for theme in themes:
        print(theme)
        get_url(theme, isFirst=True)
        time.sleep(5)
