import os
import shutil
import sqlite3
from lib.base_case import BaseCase


def print_tests(a):
    if a.isdigit():
        return int(a) * 3
    return a * 3


def delete_files_from_db():
    BaseCase.change_dir_to_root()
    db_name = 'FileStorage/FileStorage.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = 'DROP TABLE IF EXISTS files'
    try:
        cursor.execute(query)
        conn.commit()
        return True
    finally:
        conn.close()


def delete_uploaded_files_after_test_teardown():
    file_storage_db_path = 'FileStorage/uploaded_files'
    shutil.rmtree(file_storage_db_path)
    os.mkdir(file_storage_db_path)
    delete_files_from_db()