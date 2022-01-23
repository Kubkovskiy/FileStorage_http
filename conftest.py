from lib.assertions import Assertions
from lib.base_case import BaseCase
import pytest
import shutil

from lib.my_requests import MyRequests


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


@pytest.fixture()
def delete_all_files():
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
    response = delete_all_files
    print('\n === Testing ===')
    yield response
    response2 = delete_all_files
    print('\n === Deleting all files from file storage ===')
    return response2

