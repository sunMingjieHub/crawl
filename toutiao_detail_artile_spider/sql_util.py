import sqlite3

conn = sqlite3.connect('article.db')
cursor = conn.cursor()
# cursor.execute('create table article (id varchar(20) primary key, arttype varchar(20),theme varchar(20), code varchar(20),title varchar(20))')
#cursor.execute('CREATE UNIQUE INDEX artidindex on article (id);')
fp = open('toutiao_cat_data.txt', 'r+')
for lines in fp:
    temp = lines.split('_!_')
    article_id = temp[0]
    code = temp[1]
    them = temp[2]
    title = temp[3]
    cursor.execute('insert into article (id, arttype,theme,code,title) values (?, ?,?,?,?)',
                   (article_id, "0", them, code, title))

cursor.close()
conn.commit()
conn.close()