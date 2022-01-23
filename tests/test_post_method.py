import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestPostMethod(BaseCase):
    def setup_class(cls):
        print('\nStart TestPostMethod class\n')

    def teardown_class(cls):
        print('\n Delete all posted files from server')
        print('\n _______ ТИПО УДАЛИЛ ВСЕ С СЕРВЕРА _______')

        print('\n Finish TestPostMethod class')

    @pytest.mark.parametrize('file_for_test', BaseCase.get_files())
    def test_post_files_with_empty_data(self, file_for_test: str):
        file_dict = self.open_file_from_upload_folder(file_for_test)
        data, headers, payload = self.set_data_to_post_method(file_dict)
        response = MyRequests.post("upload", data, headers, payload)
        # # print(response.json())
        Assertions.base_assertions(response)
        # Check id equal name
        r_name, r_id, r_tag = response.json()['name'], response.json()['id'], response.json()['tag']
        expected_ctype = 'multipart/form-data'
        assert str(r_id) == r_name, f"'name' should be the same as 'id' = {r_id}, actual name={r_name}"
        Assertions.assert_json_value_by_name(response, 'tag', None, f"Response 'tag' should be None, actual {r_tag}")
        Assertions.assert_json_value_by_name(response, 'mimeType', expected_ctype, f"Response 'mimeType' should be \
                                                                    'multipart/form-data', actual {expected_ctype}")

    @pytest.mark.parametrize('ctype', ['auto', 'test_ctype'])
    def test_content_type(self, ctype: str):
        file_for_test = 'test4.pdf'
        file_dict = self.open_file_from_upload_folder(file_for_test)
        data, headers, payload = self.set_data_to_post_method(file_dict, content_type=ctype)
        response = MyRequests.post("upload", data, headers, payload)
        # print(response.json())
        Assertions.base_assertions(response)
        # Check id equal name
        mime_type = response.json()['mimeType']
        expected_ctype = 'test_ctype' if ctype == 'test_ctype' else 'application/pdf'
        Assertions.assert_json_value_by_name(response, 'mimeType', expected_ctype, f"Response 'mimeType' should be \
                                                                    'multipart/form-data', actual {mime_type}")

    @pytest.mark.parametrize('file_id', [999, 1])
    def test_post_with_id(self, file_id: int):
        file_for_test = 'test4.pdf'
        file_dict = self.open_file_from_upload_folder(file_for_test)
        data, headers, payload = self.set_data_to_post_method(file_dict, file_id=file_id)
        response = MyRequests.post("upload", data, headers, payload)
        # print(response.json())
        Assertions.base_assertions(response)
        # Check id equal name
        r_name, r_id = response.json()['name'], response.json()['id']
        Assertions.assert_json_value_by_name(response, 'id', file_id,
                                             f"Response 'id' expected {file_id} , actual {r_id}")
        assert str(r_id) == r_name, f"'name' should be the same as 'id' = {r_id}, actual name={r_name}"

    @pytest.mark.parametrize('name',  ['test1', 'test2', 'test3', 'test4', '1222111'])
    def test_post_with_name(self, name: (str, int)):
        file_for_test = 'test4.pdf'
        file_dict = self.open_file_from_upload_folder(file_for_test)
        data, headers, payload = self.set_data_to_post_method(file_dict, name=name, content_type='auto')
        response = MyRequests.post("upload", data, headers, payload)
        # print(response.json())
        Assertions.base_assertions(response)
        # Check id equal name
        exp_name = name
        r_name = response.json()['name']
        Assertions.assert_json_value_by_name(response, 'name', exp_name,
                                             f"Response 'name' expected {exp_name} , actual {r_name}")

