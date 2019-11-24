from lxml import etree
from selenium import webdriver
import re
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
url =['https://www.toutiao.com/ch/news_tech/']
# options.add_argument('-headless')
# options.add_argument("--proxy-server=http://202.20.16.82:10152")
options = webdriver.FirefoxOptions()
profile = webdriver.FirefoxProfile()
browser = webdriver.Firefox(options=options, firefox_profile=profile)

def get_url(url):
    browser.get(url)
    browser.implicitly_wait(5)
    response = browser.page_source

   # browser.add_cookie(cookies)
    # print(browser.add_cookie(cookies))
    print(response)
    html = etree.HTML(response)
    select = html.xpath('//div[@id="json"]/text()')
    print(select)


get_url(url[0])



#
# def get_url(url):
#     browser.get(url)
#     browser.implicitly_wait(10)
#     for i in range(2):
#         # 设置下拉次数模拟下拉滚动条加载网页
#         browser.execute_script("window.scrollBy(0,700)")
#         browser.implicitly_wait(2)
#
#
# def getlink():
#     """
#     拿到每篇文章的链接
#     :return:
#     """
#     url = 'https://www.toutiao.com/ch/nba/'
#     url = 'https://www.toutiao.com/ch/news_tech/'
#     browser.get(url)
#     # 设置隐式等待，最多等待10s
#     browser.implicitly_wait(5)
#     # 模拟鼠标拖动
#     for x in range(50):
#         js = "var q=document.documentElement.scrollTop=" + str(x * 700)
#         browser.execute_script(js)
#         time.sleep(2)
#     time.sleep(5)
#     #链接数组
#     links=[]
#     response = browser.page_source
#     print(response)
#     #browser.close()
#     soup = BeautifulSoup(response, 'lxml')
#     groups = soup.find_all(class_='link')
#     print(len(groups))
#     # for group in groups:
#     #     links.append(BASE_URL+group.attrs['href'])
#     # return links
#
# # get_url("https://www.toutiao.com/ch/news_tech/")
# getlink()
browser.quit()

