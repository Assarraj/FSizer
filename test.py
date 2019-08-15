import sqlite3 as sq

conn = sq.connect("files.db")

conn.row_factory = sq.Row
cur = conn.cursor()


cur.execute("SELECT path FROM 'paths' ORDER BY path_ID")


res = cur.fetchall()

for row in res:
    print(row['path'])

