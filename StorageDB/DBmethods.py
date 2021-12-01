from models import conn, cur


def add_to_db(connect=conn, cursor=cur, **kwargs):
    """Функция для заполнения таблицы"""
    cursor.execute("""INSERT INTO files(file_id, name, tag, size, mimeType, modificationTime) \
    VALUES(?, ?, ?, ?, ?, ?), ;""", kwargs["file_id"], kwargs["name"], kwargs["size"],
                kwargs["mimeType"], kwargs["modificationTime"])
    connect.commit()
    cur.close()
    connect.close()
