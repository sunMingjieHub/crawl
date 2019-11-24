import requests
import json
import csv
import math
import time
import hashlib


def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS,CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
  #  print("AS:"+AS,"CP:"+CP)
    return AS,CP



headers = {
    "Host": "www.toutiao.com",
    "Connection": "keep-alive",
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
}

fp = open("articleId.csv","wt",newline='',encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('article_id','max_behot_time'))


themes = [
    'news_travel',
    'news_food',
    'news_tech',
    'news_game',
    'news_entertainment',
    'news_sports',
    'news_finance',
    'news_military',
    'news_history',
]


def get_url(theme, max_behot_time, AS, CP):
    url = 'https://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1' \
           '&max_behot_time={1}' \
           '&max_behot_time_tmp={1}' \
           '&tadrequire=true' \
           '&as={2}' \
           '&cp={3}'.format(theme,max_behot_time,AS,CP)
    return url


def get_item(url):
    print(url)
    next_max_behot_time = -1
    cookies = {
        "tt_webid":"6413971664988276225"
    }
    web = requests.get(url, headers=headers, cookies=cookies)
    print(web.text)
    time.sleep(3)
    js_wb = json.loads(web.text)
    if js_wb["message"] == "success":
        datas = js_wb["data"]
        next_max_behot_time = js_wb["next"]["max_behot_time"]
        for article in datas:
            article_id = article["item_id"]
            writer.writerow((article_id, next_max_behot_time))
    return next_max_behot_time


if __name__ == '__main__':
    # 获取新闻url
    for theme in themes:
        max_behot_time = 0
        while max_behot_time != -1:
            AS, CP = getASCP()
            url = get_url(theme, max_behot_time, AS, CP)
            max_behot_time = get_item(url)

            print(max_behot_time)
    fp.close()


    # # 获取新闻详细信息
    # web = requests.get('http://toutiao.com/group/6759429903407383053',headers =headers)
    # soup = BeautifulSoup(web.text,"html.parser")
    # scripts = soup.find_all("script")
    # for s in scripts:
    #     info = re.findall("<script>var BASE_DATA =(.*?);</script>",str(s),re.S)
    #     if len(info) != 0:
    #         print(info[0])
    #         title = re.findall("title: '&quot;(.*?)&quot;'", info[0], re.S)
    #         title= title[0] + ".txt"
    #         content = re.findall("content: '&quot;(.*?)&quot;'", info[0], re.S)
    #         content = re.sub("\\\\u003.*?\\\\u003E","\n",content[0])
    #         with open(title,"w") as fp:
    #             fp.write(content)
    #             fp.close()


