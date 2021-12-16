import sqlite3

DB_NAME = 'FileStorage.db'


class DBconnect:
    @staticmethod
    def connect_to_db(func):
        """connect to DB and create cursor, commit, after will close connection"""

        def inner_func(self, *args, **kwargs):
            self.conn = sqlite3.connect(DB_NAME)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            try:
                res = func(self, *args, **kwargs)
                return res
            finally:
                self.cursor.close()
                self.conn.close()

        return inner_func

    def __init__(self):

        self.create_table()

    @connect_to_db
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS files(
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                tag TEXT,
                                size INTEGER,
                                mimeType TEXT,
                                modificationTime TEXT);""")
        self.conn.commit()

    @connect_to_db
    def add_to_db(self, params: dict):
        try:
            query = "INSERT INTO files(id, name, tag, size, mimeType, modificationTime) \
                    VALUES(?, ?, ?, ?, ?, ?);"
            data = list(params.values())
            self.cursor.execute(query, data)
            self.conn.commit()
            return params
        except sqlite3.IntegrityError as err:
            if str(err) == 'UNIQUE constraint failed: files.id':
                query = "UPDATE files SET id=?, name=?, tag=?, size=?, mimeType=?, " \
                        "modificationTime=? WHERE id = ?;"
                data.append(params['id'])
                self.cursor.execute(query, data)
                self.conn.commit()
                return params

    @connect_to_db
    def return_next_id(self) -> str:
        query = 'SELECT id FROM files'
        all_id = max(self.cursor.execute(query).fetchall())[0]

        return str(all_id + 1)

    @connect_to_db
    def parse_from_db(self, params: dict):
        my_dict = {"payload":{}}
        for key, value in params.items():
            amount_items = ', '.join('?' * len(value))
            query = 'SELECT * FROM files WHERE ({0}) in ({1})'.format(key, amount_items)
            self.cursor.execute(query, value)
            result = self.cursor.fetchall()
            my_dict['payload'].update(dict(result[0]))
        return my_dict