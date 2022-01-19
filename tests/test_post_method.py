import os

import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import requests
import pytest


# @pytest.fixture(scope='class')
# def prepair_files_for_upload():
#     url_to_archive = "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"
#     files = BaseCase.download_and_extract_zip_archive_from_cloud(url_to_archive)
#     print(files)


class TestPostMethod(BaseCase):
    def setup_method(self, test_method):
        url_to_archive = "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"
        self.files = self.download_and_extract_zip_archive_from_cloud(url_to_archive)


    def teardown_method(self, test_method):
        import shutil
        shutil.rmtree(BaseCase.FILES_FOR_UPLOAD)


    def test_is_file_in_dir(self):
        print(os.listdir('tests/files_for_upload/'))
        assert self.files == os.listdir('tests/files_for_upload/'), f'что то не так'


    def test_post_with_empty_data(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        response_from_cloud = self.download_file_from_cloud(file_url)
        content_type = response_from_cloud.headers.get('Content-Type')
        file_from_cloud = response_from_cloud.content
        headers = {
            'Content-Disposition': response_from_cloud.headers.get('Content-Disposition'),
            'Content-Length': response_from_cloud.headers.get('Content-Length'),
        }
        payload = {"file": file_from_cloud}
        data = {"name": None, "tag": None, "id": None, "content-type": content_type}
        response = MyRequests.post("upload", data, headers, payload)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id', 'name', 'tag', 'size',
                                                   'mimeType', 'modificationTime'])

    def test_post_with_id(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        response_from_cloud = self.download_file_from_cloud(file_url)
        content_type = response_from_cloud.headers.get('Content-Type')
        file_from_cloud = response_from_cloud.content
        headers = {
            'Content-Disposition': response_from_cloud.headers.get('Content-Disposition'),
            'Content-Length': response_from_cloud.headers.get('Content-Length'),
                }
        payload = {"file": file_from_cloud}
        file_id = 1
        data = {"name": None, "tag": None, "id": file_id, "content-type": content_type}
        response = MyRequests.post("upload", data, headers, payload)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id', 'name', 'tag', 'size',
                                                   'mimeType', 'modificationTime'])
        Assertions.assert_json_value_by_name(response, "id", file_id,
                        f"'id' should be equal = {file_id}, but actual id={response.json()['id']}")

    def test_post_with_name(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        response_from_cloud = self.download_file_from_cloud(file_url)
        content_type = response_from_cloud.headers.get('Content-Type')
        file_from_cloud = response_from_cloud.content
        headers = {
            'Content-Disposition': response_from_cloud.headers.get('Content-Disposition'),
            'Content-Length': response_from_cloud.headers.get('Content-Length'),
        }
        payload = {"file": file_from_cloud}
        name = 'test_name'
        data = {"name": name, "tag": None, "id": None, "content-type": content_type}
        response = MyRequests.post("upload", data, headers, payload)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id', 'name', 'tag', 'size',
                                                   'mimeType', 'modificationTime'])
        Assertions.assert_json_value_by_name(response, "name", name,
                        f"'name' should be equal 'id' = {name}, but actual name={response.json()['name']}")

    def test_post_with_name_and_id(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        response_from_cloud = self.download_file_from_cloud(file_url)
        content_type = response_from_cloud.headers.get('Content-Type')
        file_from_cloud = response_from_cloud.content
        headers = {
            'Content-Disposition': response_from_cloud.headers.get('Content-Disposition'),
            'Content-Length': response_from_cloud.headers.get('Content-Length'),
        }
        payload = {"file": file_from_cloud}
        name = 'test_name'
        file_id = 15
        data = {"name": name, "tag": None, "id": file_id, "content-type": content_type}
        response = MyRequests.post("upload", data, headers, payload)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id', 'name', 'tag', 'size',
                                                   'mimeType', 'modificationTime'])
        Assertions.assert_json_value_by_name(response, "name", name,
                        f"'name' should be equal 'id' = {name}, but actual name= {response.json()['name']}")
        Assertions.assert_json_value_by_name(response, "id", file_id,
                        f"'id' should be equal = {file_id}, but actual id={response.json()['id']}")

        # Assertions.assert_json_value_by_name(response, "name", str(file_id),
        #                                      f"'name' should be equal 'id' = {file_id}, but 'name'= {response.json()['name']}")
