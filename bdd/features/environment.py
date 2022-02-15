import os
import shutil
import sqlite3

from bdd.main import delete_files_from_db, delete_uploaded_files_after_test_teardown
from lib.base_case import BaseCase

# FILES_FOR_UPLOAD = "tests/files_for_upload/"
# BASE_SERVER_URL = "http://127.0.0.1:9000/api/"
# URL_TO_ARCHIVE = "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"
# BASE_KEYS = ['id', 'name', 'tag', 'size', 'mimeType', 'modificationTime']
# FILES_LIST = ['test1.docx', 'test2.xlsx', 'test3.txt', 'test4.pdf', 'test5.jpg']


def before_all(contex):
    files_for_upload = BaseCase.get_files()
    contex.files = files_for_upload
    if len(contex.files) == 0:
        raise Exception('There are no files in upload_folders')
    print('\nbefore all\n--Download files from cloud--\n')


def before_feature(contex, feature):
    delete_files_from_db()
    print('before features\n--Deleting files from server and clean DB--\n')


def after_feature(contex, feature):
    delete_uploaded_files_after_test_teardown()
    print('after features\n--Deleting uploaded to server files and clean DB--\n')


def after_all(contex):
    # delete tests/files_for_upload/
    BaseCase.delete_upload_files(BaseCase.FILES_FOR_UPLOAD)
    print('after all\n--Deleting uploaded files from "tests/uploader_files"--\n')
