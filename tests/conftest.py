from lib.base_case import BaseCase
import pytest


@pytest.fixture(scope='session', autouse=True)
def preparing_files_for_upload_and_delete_after_session():
    files = BaseCase.get_files()
    yield files
    # delete tests/files_for_upload/
    BaseCase.delete_upload_files()


@pytest.fixture(scope='class', autouse=True)
def delete_files_from_server():
    BaseCase.delete_all_files_from_server()
    yield
    # delete files from FileStorage
    BaseCase.delete_all_files_from_server()
