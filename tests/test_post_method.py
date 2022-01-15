from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import requests


class TestPostMethod(BaseCase):
    def test_post_method_with_empty_data(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        content_type, headers, file_from_cloud = self.download_file_from_cloud(file_url)
        file = {"file": file_from_cloud}
        data = {"name": None, "tag": None, "id": None, "content-type": content_type}
        response = MyRequests.post("upload", data, headers, file)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id', 'name', 'tag', 'size',
                                                   'mimeType', 'modificationTime'])
