import sqlite3
import os
db_path = 'menu.db'
conn = sqlite3.connect(db_path)
#print(conn)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS menus (id, name, price)")

c.execute("INSERT INTO menus VALUES (1, 'Espresso', 3800)")

c.execute("SELECT * FROM menus")

print(c.fetchone())
conn.commit()
c.close()
conn.close()

