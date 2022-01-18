from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import requests


class TestPostMethod(BaseCase):
    def test_post_with_empty_data(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        content_type, headers, file_from_cloud = self.download_file_from_cloud(file_url)
        payload = {"file": file_from_cloud}
        data = {"name": None, "tag": None, "id": None, "content-type": content_type}
        response = MyRequests.post("upload", data, headers, payload)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id', 'name', 'tag', 'size',
                                                   'mimeType', 'modificationTime'])

    def test_post_with_id(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        content_type, headers, file_from_cloud = self.download_file_from_cloud(file_url)
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
        content_type, headers, file_from_cloud = self.download_file_from_cloud(file_url)
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
        content_type, headers, file_from_cloud = self.download_file_from_cloud(file_url)
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
