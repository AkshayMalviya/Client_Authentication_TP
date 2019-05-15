import sqlite3
#Change Database name and Values in Insert Statement and also need to change database name in get_from_table.py same as here
conn = sqlite3.connect('test1.db')  
c = conn.cursor()
c.execute(''' CREATE TABLE users (uname,upass) ''')

c.execute("INSERT INTO users(uname,upass) VALUES ('username1','password1'),('username2','password2'),('username3','password3')")

conn.commit()

conn.close()