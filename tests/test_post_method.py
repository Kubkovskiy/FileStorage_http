from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import requests


class TestPostMethod(BaseCase):
    def test_post_method(self):
        file_url = "https://disk.yandex.ru/i/2xwFm2zp34nzZA"
        data_from_cloud = self.download_file_from_cloud(file_url)
        headers_dict = data_from_cloud.headers
        headers = {
            'Content-Disposition': headers_dict['Content-Disposition'],
            'Content-Length': headers_dict['Content-Length'],
                }
        file = {"file": data_from_cloud.content}
        data = {"name": None, "tag": None, "id": None, "content-type": "application/pdf"}
        response = MyRequests.post("upload", data, headers, file)
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, ['id','name','tag','size',
                                                   'mimeType', 'modificationTime'])
W