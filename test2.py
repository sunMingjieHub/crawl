from selenium import webdriver
import time
import random

from selenium.common.exceptions import NoSuchElementException

options = webdriver.FirefoxOptions()
profile = webdriver.FirefoxProfile()

## 第二步：开启“手动设置代理”
profile.set_preference('network.proxy.type', 1)
## 第三步：设置代理IP
profile.set_preference('network.proxy.http', '138.197.104.219')
## 第四步：设置代理端口，注意端口是int类型，不是字符串
profile.set_preference('network.proxy.http_port', 8080)

browser = webdriver.Firefox(options=options, firefox_profile=profile)


def isElementPresent(driver, value):

    """
    用来判断元素标签是否存在，
    """
    try:
       # print(driver.page_source)
        element = driver.find_element_by_xpath(value)
       # print(value)
    # 原文是except NoSuchElementException, e:
    except NoSuchElementException as e:
        # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
        return False
    else:
        # 没有发生异常，表示在页面中找到了该元素，返回True
        return True


browser.get('http://icanhazip.com')
browser.implicitly_wait(5)

browser.get('https://www.toutiao.com/a6760618370665545997/')
browser.implicitly_wait(5)
time.sleep(3)
for i in range(3):
    js = f"var q=document.documentElement.scrollTop={random.randint(30, 10000)}"
    browser.execute_script(js)
    time.sleep(1)

if isElementPresent(browser,'//div[@class="article-content"]'):
    print('content')
    content = browser.find_element_by_xpath('//div[@class="article-content"]').text
elif isElementPresent(browser,'//div[@class="a-con"]'):
    print('a-con')
    content = browser.find_element_by_xpath('//div[@class="a-con"]').text
elif isElementPresent(browser,'//div[@class="answers"]'):
    print('answer')
    contents = browser.find_elements_by_xpath('//div[@class="answer-text-full rich-text"]')
    ss = ""
    for c in contents:
        ss=ss+c.text
    print(ss)
else:
    try:
        content = browser.find_element_by_xpath('//article').text
        print('//article')
    except:
        print("NoElementException:", browser.current_url)
        pass
time.sleep(5)
browser.quit()
