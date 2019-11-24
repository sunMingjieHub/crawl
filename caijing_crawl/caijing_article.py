import requests
from lxml import etree
import json
import random
from multiprocessing.pool import Pool
import threading

ips=[]
mark =0
root_url = 'http://www.yinhangcn.com'
hearders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

lock_mark = threading.Lock()


def get_proxy():
    global ips
    f = open('verified_proxies.json', 'r+')
    for line in f:
        jd = json.loads(line)
        proxy = {jd['type']:jd['host']+":"+str(jd['port'])}
        ips.append(proxy)
    f.close()


def get_urls():
    global mark
    with open("mark.csv") as csvfile:
        mLines = csvfile.readlines()
    targetLine = mLines[-1]

    try:
        lock_mark.acquire()
        mark=int(targetLine.split(',')[0])
    finally:
        lock_mark.release()
    i =0
    ids=[]
    with open('caijing.txt','r+') as fp:
        for lines in fp:
            i=i+1
            if i<mark:
                continue
            temp = lines.split('_!_')
            if len(temp)>1:
                #print(temp)
                art_url = temp[2]
                id =temp[2][6:-5]
                title = temp[0]
                ids.append({'article_id':id,'title':title,'url':art_url})
    print(len(ids))

    return ids


def get_articles(article):
    global mark
    proxy = random.choice(ips)
    url = root_url + article['url']
    print(url)
    resp = requests.get(url, hearders, proxies=proxy)
    web = etree.HTML(resp.text)
    try:
        contents = web.xpath('//div[@class="newscontent"]')[0]
        content = contents.xpath('string(.)')
        content = str(content).split()[0]

    except Exception as e:
        print(e)
        print(resp.text)
        content=" "
    finally:
        title = "caijing/" + article['article_id'] + article['title'] + ".txt"
        title = "".join(title.split(' '))
        with open(title, 'w') as fp:
            fp.write(content)
        try:
            lock_mark.acquire()
            with open('mark.csv', 'a+') as f2:
                mark = mark + 8
                f2.write('\n')
                f2.write(str(mark))
        finally:
            lock_mark.release()


if __name__ == '__main__':
    get_proxy()
    articles = get_urls()
    pool = Pool(processes=8)
    pool.map(get_articles,articles)