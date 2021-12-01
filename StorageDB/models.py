import sqlite3

conn = sqlite3.connect('FileStorage.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS files(
                        base_id INT PRIMARY KEY,
                        file_id INT,
                        name TEXT,
                        tag TEXT,
                        size INT,
                        mimeType TEXT,
                        modificationTime TEXT);""")
conn.commit()
conn.close()
