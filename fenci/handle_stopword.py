import redis
if __name__ == '__main__':
    rd= redis.Redis("10.108.36.113")
    # a = ""
    # print(rd.sismember("stopword" , a))

    with open('stopwords.txt','r') as f:
        lines = f.readlines()
        for word in lines:
            wb = word.encode('utf-8').strip()
            if wb != b'':
                print(wb)
                rd.sadd("stopword",wb)

