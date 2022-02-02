from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import pytest
import shutil
import os


@pytest.fixture(scope='session', autouse=True)
def preparing_files_for_upload_and_delete_after_test():
    BaseCase.delete_all_files_from_server()
    files = BaseCase.get_files()
    yield files
    # delete files from FileStorage
    BaseCase.delete_all_files_from_server()
    # delete tests/files_for_upload/
    BaseCase.delete_upload_files()