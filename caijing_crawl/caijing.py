import requests
import json
url = 'http://news.yinhangcn.com/touzi/'
hearders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
urls = [
    'http://news.yinhangcn.com/api/ajaxlist_encid.php?cid=touzi&size=4010',
    'http://news.yinhangcn.com/api/ajaxlist_encid.php?cid=licai&size=2620',
    'http://news.yinhangcn.com/api/ajaxlist_encid.php?cid=bank&size=8200',
    'http://news.yinhangcn.com/api/ajaxlist_encid.php?cid=waihui&size=4850',
    ]

for url in urls:
    resp= requests.get(url,hearders)
    web = json.loads(resp.text)
    datas= web['data']
    print(len(datas))
    with open('caijing.txt','a+') as fp:
        for data in datas:
            title = data['title'].strip()
            url = data['url']
            theme ='new_finance'
            fp.write(title+"_!_"+theme+"_!_"+url)
            fp.write('\n')
# print(datas)
