import sqlite3

DB_NAME = 'FileStorage.db'


class DBconnect:
    @staticmethod
    def connect_to_db(func):
        """connect to DB and create cursor, commit, after will close connection"""

        def inner_func(self, *args, **kwargs):
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
            try:
                res = func(self, *args, **kwargs)
                self.conn.commit()
            finally:
                self.cursor.close()
                self.conn.close()

        return inner_func

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_table()

    @connect_to_db
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS files(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                file_id TEXT,
                                name TEXT,
                                tag TEXT,
                                size INTEGER,
                                mimeType TEXT,
                                modificationTime TEXT);""")

    @connect_to_db
    def add_to_db(self, params: dict):
        query = "INSERT INTO files(file_id, name, tag, size, mimeType, modificationTime) \
                VALUES(?, ?, ?, ?, ?, ?);"
        data = list(params.values())
        self.cursor.execute(query, data)
