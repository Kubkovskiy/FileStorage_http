import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestDeleteMethod(BaseCase):

    def setup_class(cls):
        print('\n === Start TestDeleteMethod ===')
        print('\n === Deleting all files from file storage ===')
        response = BaseCase.delete_all_files()
        print(response.json())
        # Assertions.assert_expected_status_code(response, 200)

        # Assertions.assert_json_value_by_name(response, 'message', "No result", "Unexpected message")
        print('\n === Testing ===')

    @pytest.mark.parametrize('expected_file_id', [1, 2, 3, 4, 5])
    def test_delete_by_id(self, expected_file_id):
        file_id = 1
        files_for_test = BaseCase.get_files()
        for file in files_for_test:
            response = self.upload_file_for_delete_test(file, file_id=file_id)
            file_id += 1
        response2 = MyRequests.get('get')
        Assertions.base_assertions_for_get_method(response2)
        content_list = response2.json()
        for content in content_list:
            content_id = content['id']
            if content_id == expected_file_id
                break
            assert expected_file_id in content, f"Unexpected id - {content['id']}, expected {expected_file_id}"
        response3 = MyRequests.delete('delete', file_id=expected_file_id)




        print(response.text)
        assert response.status_code == 404, f'что то не то'

    # @pytest.mark.parametrize('ctype', ['auto', 'test_ctype'])
    # def test_content_type(self, ctype: str):
    #     file_for_test = 'test4.pdf'
    #     file_dict = self.open_file_from_upload_folder(file_for_test)
    #     data, headers, payload = self.set_data_to_post_method(file_dict, content_type=ctype)
    #     response = MyRequests.post("upload", data, headers, payload)
    #     # print(response.json())
    #     Assertions.base_assertions(response)
    #     # Check id equal name
    #     mime_type = response.json()['mimeType']
    #     expected_ctype = 'test_ctype' if ctype == 'test_ctype' else 'application/pdf'
    #     Assertions.assert_json_value_by_name(response, 'mimeType', expected_ctype, f"Response 'mimeType' should be \
    #                                                                 'multipart/form-data', actual {mime_type}")
    #
    # @pytest.mark.parametrize('file_id', [999, 1])
    # def test_post_with_id(self, file_id: int):
    #     file_for_test = 'test4.pdf'
    #     file_dict = self.open_file_from_upload_folder(file_for_test)
    #     data, headers, payload = self.set_data_to_post_method(file_dict, file_id=file_id)
    #     response = MyRequests.post("upload", data, headers, payload)
    #     # print(response.json())
    #     Assertions.base_assertions(response)
    #     # Check id equal name
    #     r_name, r_id = response.json()['name'], response.json()['id']
    #     Assertions.assert_json_value_by_name(response, 'id', file_id,
    #                                          f"Response 'id' expected {file_id} , actual {r_id}")
    #     assert str(r_id) == r_name, f"'name' should be the same as 'id' = {r_id}, actual name={r_name}"
    #
    # @pytest.mark.parametrize('name', ['test1', 'test2', 'test3', 'test4', 1222111])
    # def test_post_with_name(self, name: (str, int)):
    #     file_for_test = 'test4.pdf'
    #     file_dict = self.open_file_from_upload_folder(file_for_test)
    #     data, headers, payload = self.set_data_to_post_method(file_dict, name=name, content_type='auto')
    #     response = MyRequests.post("upload", data, headers, payload)
    #     # print(response.json())
    #     Assertions.base_assertions(response)
    #     # Check id equal name
    #     exp_name = name
    #     r_name = response.json()['name']
    #     Assertions.assert_json_value_by_name(response, 'name', str(exp_name),
    #                                          f"Response 'name' expected {exp_name} , actual {r_name}")
    #
    # @pytest.mark.parametrize('tag', ['test1', 'test2', 'test3', 'test4', '1222111'])
    # def test_post_with_tag(self, tag: str):
    #     file_for_test = 'test4.pdf'
    #     file_dict = self.open_file_from_upload_folder(file_for_test)
    #     data, headers, payload = self.set_data_to_post_method(file_dict, tag=tag, content_type='auto')
    #     response = MyRequests.post("upload", data, headers, payload)
    #     # print(response.json())
    #     Assertions.base_assertions(response)
    #     # Check id equal name
    #     exp_tag = tag
    #     r_tag = response.json()['tag']
    #     Assertions.assert_json_value_by_name(response, 'tag', exp_tag,
    #                                          f"Response 'tag' expected {exp_tag} , actual {r_tag}")
    #
    # @pytest.mark.parametrize('file_id', [1, 999, 999])
    # @pytest.mark.parametrize('name', ['test_valid_name', 'test_valid_name', 1222111])
    # @pytest.mark.parametrize('tag', ['test_tag', 'test_tag', 5555])
    # def test_post_with_id_name_tag(self, file_id: int, name: (str, int), tag: (str, int)):
    #     file_for_test = 'test4.pdf'
    #     file_dict = self.open_file_from_upload_folder(file_for_test)
    #     data, headers, payload = self.set_data_to_post_method(file_dict,
    #                                                           file_id=file_id,
    #                                                           name=name,
    #                                                           tag=tag,
    #                                                           content_type='auto')
    #     response = MyRequests.post("upload", data, headers, payload)
    #     # print(response.json())
    #     Assertions.base_assertions(response)
    #     # Check id equal name
    #     r_dict = response.json()
    #     r_file_id, r_tag, r_name = r_dict['id'],r_dict['name'], r_dict['tag']
    #     Assertions.assert_json_value_by_name(response, 'id', file_id,
    #                                          f"Response 'id' expected {file_id} , actual {r_file_id}")
    #     Assertions.assert_json_value_by_name(response, 'name', str(name),
    #                                          f"Response 'name' expected {name} , actual {r_name}")
    #     Assertions.assert_json_value_by_name(response, 'tag', str(tag),
    #                                          f"Response 'name' expected {tag} , actual {r_tag}")
