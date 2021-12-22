import sqlite3


DB_NAME = 'FileStorage.db'





class DBconnect:

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

    def fetch_all(self):
        self.cursor.execute('select * from files')
        res = self.cursor.fetchall()
        result = [dict(i) for i in res]
        return result

    @staticmethod
    def return_next_id() -> str:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            query = 'SELECT id FROM files'
            all_id = cursor.execute(query).fetchall()
            if len(all_id) == 0:
                return '1'
            all_id = max(cursor.execute(query).fetchall())[0]
            return str(all_id + 1)
        finally:
            conn.close()

    @connect_to_db
    def parse_from_db(self, params: dict = None):
        if not params:
            return self.fetch_all()
        query_base = 'SELECT * FROM files WHERE '
        my_filter = ''
        count = 1
        values = []
        result_dict = {}
        for key, value in params.items():
            my_filter += f'{key} in ({", ".join("?" * len(value))})'
            for i in value:
                values.append(i)
            if count < len(params):
                my_filter += ' AND '
                count += 1
        query = query_base + my_filter
        self.cursor.execute(query, values)
        res = self.cursor.fetchall()
        result = [dict(i) for i in res]
        return result

    @connect_to_db
    def delete_from_db(self, params: dict = None):
        query_select = 'SELECT * FROM files WHERE '
        query_delete = 'DELETE FROM files WHERE '
        my_filter = ''
        count = 1
        values = []
        result_dict = {}
        for key, value in params.items():
            my_filter += f'{key} in ({", ".join("?" * len(value))})'
            for i in value:
                values.append(i)
            if count < len(params):
                my_filter += ' AND '
                count += 1
        self.cursor.execute(query_select + my_filter, values)
        res = self.cursor.fetchall()
        result = [dict(i) for i in res]
        self.cursor.execute(query_delete + my_filter, values)
        self.conn.commit()
        return result
