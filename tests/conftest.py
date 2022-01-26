from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import pytest
import shutil
import os


@pytest.fixture(scope='session')
def preparing_files_for_upload():
    """download from public link and extract to tests/files_for_upload/ folder
    after tests folder should be deleted '"""
    print('\n === Start session ===')
    print(f'\n Download files from {BaseCase.URL_TO_ARCHIVE} ')
    print(f'\n Extract archive to {BaseCase.FILES_FOR_UPLOAD} ')
    # files = BaseCase.download_and_extract_zip_archive_from_cloud(URL_TO_ARCHIVE)
    # print(' \n === TESTING === \n')
    yield
    # delete upload folder
    print("\n Deleting upload folder")
    # shutil.rmtree(BaseCase.FILES_FOR_UPLOAD)
    print('\n === Finish session === \n')


@pytest.fixture(scope="session")
def get_files() -> list:
    BaseCase.change_dir_to_root()
    folder_path = BaseCase.FILES_FOR_UPLOAD
    if os.path.isdir(folder_path) and len(os.listdir(folder_path)) > 0:
        return os.listdir(folder_path)
    files = BaseCase.download_and_extract_zip_archive_from_cloud(BaseCase.URL_TO_ARCHIVE)
    return files


@pytest.fixture(scope='session')
def delete_upload_files():
    BaseCase.change_dir_to_root()
    if os.path.isdir(BaseCase.FILES_FOR_UPLOAD):
        shutil.rmtree(BaseCase.FILES_FOR_UPLOAD)


@pytest.fixture()
def delete_all_files_from_server():
    response = MyRequests.get('get')
    assert response.status_code in (200, 404), f"Unexpected status code. Expected: 200 or 204,\
                                                                Actual: {response.status_code}"
    if response.status_code == 404:
        return response
    all_id = BaseCase.get_file_id_from_server(response)
    data = {'id': all_id}
    response = MyRequests.delete('delete', data)
    Assertions.assert_expected_status_code(response, 200)
    return response


@pytest.fixture(scope='session')
def delete_all_files_from_upload_folder():
    response = MyRequests.get('get')
    assert response.status_code in (200, 204), f"Unexpected status code. Expected: 200 or 204,\
                                                                Actual: {response.status_code}"
    if response.status_code == 204:
        return response
    all_id = BaseCase.get_file_id_from_server(response)
    data = {'id': all_id}
    response = MyRequests.delete('delete', data)
    Assertions.assert_expected_status_code(response, 200)
    return response

@pytest.fixture(scope='class')
def delete_all_from_server_before_and_after_test(delete_all_files):
    print('\n === Start session ===')
    print('\n === Deleting all files from file storage ===')
    response = delete_all_files_from_upload_folder
    print('\n === Testing ===')
    yield response
    response2 = delete_all_files_from_upload_folder
    print('\n === Deleting all files from file storage ===')
    return response2

