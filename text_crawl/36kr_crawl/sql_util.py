import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("create table user( id varchar(20),name varchar(20)")
print(cursor.rowcount)
cursor.close()