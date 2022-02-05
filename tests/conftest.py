import os
import sqlite3
import shutil
from lib.base_case import BaseCase
import pytest


def delete_files_from_db():
    print('delete from fixture')
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


@pytest.fixture(scope='session', autouse=True)
def preparing_files_for_upload_and_delete_after_session():
    files = BaseCase.get_files()
    yield files
    # delete tests/files_for_upload/
    BaseCase.delete_upload_files(BaseCase.FILES_FOR_UPLOAD)


@pytest.fixture(scope='class', autouse=True)
def delete_files_from_server_setup(request):
    delete_files_from_db()

    def delete_uploaded_files_after_test_teardown():
        file_storage_db_path = 'FileStorage/uploaded_files'
        shutil.rmtree(file_storage_db_path)
        os.mkdir(file_storage_db_path)
        delete_files_from_db()
    request.addfinalizer(delete_uploaded_files_after_test_teardown)
