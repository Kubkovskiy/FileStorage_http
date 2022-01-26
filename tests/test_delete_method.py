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
        print('\n === Testing ===')

    @pytest.mark.parametrize('expected_file_id', [1, 2, 3, 4, 5])
    def test_delete_by_id(self, expected_file_id):
        # Prepare file for test then upload it with expected id
        file_for_test = self.get_files()[0]
        response = self.upload_file_for_delete_test(filename=file_for_test, file_id=expected_file_id)
        file_id_from_response = response.json()['id']
        Assertions.assert_json_value_by_name(response, 'id', expected_file_id,
                                    f" Unexpected id: {file_id_from_response}, expected:{expected_file_id}")
        # delete file by expected id
        data = {'id': expected_file_id}
        response_after_delete = MyRequests.delete('delete', data=data)
        Assertions.assert_expected_status_code(response_after_delete, 200)
        expected_message = "1 files deleted"
        actual_message = response_after_delete.json()['message']
        Assertions.assert_json_value_by_name(response_after_delete,'message',expected_message,
                                        f"Unexpected message:{actual_message}, expected:{expected_message}")
        # check is file delete
        response_get = MyRequests.get('get')
        Assertions.assert_expected_status_code(response_get, 404)
        expected_message = "No result"
        actual_message = response_get.json()['message']
        Assertions.assert_json_value_by_name(response_get, 'message', expected_message,
                                    f"Unexpected message:{actual_message}, expected:{expected_message}")

    @pytest.mark.parametrize('expected_name', ['test1', 'test2', 'test3', 'test4', 'test5'])
    def test_delete_by_name(self, expected_name):
        # Prepare file for test then upload it with expected id
        file_for_test = self.get_files()[0]
        response = self.upload_file_for_delete_test(filename=file_for_test, name=expected_name)
        name_from_response = response.json()['name']
        Assertions.assert_json_value_by_name(response, 'name', expected_name,
                                             f" Unexpected id: {name_from_response}, expected:{expected_name}")
        # delete file by expected name
        data = {'name': expected_name}
        response_after_delete = MyRequests.delete('delete', data=data)
        Assertions.assert_expected_status_code(response_after_delete, 200)
        expected_message = "1 files deleted"
        actual_message = response_after_delete.json()['message']
        Assertions.assert_json_value_by_name(response_after_delete, 'message', expected_message,
                                             f"Unexpected message:{actual_message}, expected:{expected_message}")
        # check is file delete
        response_get = MyRequests.get('get')
        Assertions.assert_expected_status_code(response_get, 404)
        expected_message = "No result"
        actual_message = response_get.json()['message']
        Assertions.assert_json_value_by_name(response_get, 'message', expected_message,
                                             f"Unexpected message:{actual_message}, expected:{expected_message}")