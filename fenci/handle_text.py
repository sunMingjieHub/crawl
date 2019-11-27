import jieba
from jieba import posseg as posg
import jieba.analyse as anls #关键词提取
import threading
import os
from multiprocessing import Pool
import redis

rd = redis.Redis("10.108.36.113")
flags =[
    'n',
    'nt',
    'nz',
]
source_path = os.path.abspath('/home/smj/PycharmProjects/crawlText/fenci/娱乐')
target_path = os.path.abspath('/home/smj/PycharmProjects/crawlText/fenci/entertain')

if not os.path.exists(target_path):
    os.makedirs(target_path)


def get_data_in_sql():
    global rd
    if os.path.exists(source_path):
        for root, firs, files in os.walk(source_path):
            for file in files:
                rd.set(file,0)


def get_all_txt():
    if os.path.exists(source_path):
        for root, firs, files in os.walk(source_path):
            return files


def cut_txt(file):
    global rd
    tag = rd.get(file)
    if tag == b'0':
        print(file)
        results = []
        with open("./娱乐/"+file,"r") as f:
            lines = f.readlines()
            for line in lines:
                words = posg.lcut(line)
                results =results+words
        results = list(set(results))
        with open("./entertain/"+file,"w") as f1:
            for word,flag in results:
                if flag not in flags:
                    continue
                if word.strip() != '':
                    if not rd.sismember('stopword',word):
                        f1.write(word+"_"+flag)
                        f1.write('\n')
        rd.set(file,1)


if __name__ == '__main__':

    # get_data_in_sql()
    all_files = get_all_txt()
    pool = Pool(processes=4)
    pool.map(cut_txt,all_files)
    # for file in all_files:
    #     cut_txt(file)

