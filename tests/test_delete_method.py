import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestDeleteMethod(BaseCase):

    @pytest.mark.parametrize('expected_file_id', [1, 2, 3, 4, 5])
    def test_delete_by_id(self, expected_file_id):
        # Prepare file for test then upload it with expected id
        file_for_test = self.get_files()[0]
        response = self.upload_file_for_test_to_file_storage(filename=file_for_test, file_id=expected_file_id)
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
        response = self.upload_file_for_test_to_file_storage(filename=file_for_test, name=expected_name)
        name_from_response = response.json()['name']
        Assertions.assert_json_value_by_name(response, 'name', expected_name,
                                             f" Unexpected name: actual {name_from_response}, expected:{expected_name}")
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

    @pytest.mark.parametrize('expected_tag', ['test1', 'test2', 'test3', 'test4', 'test5'])
    def test_delete_by_tag(self, expected_tag):
        # Prepare file for test then upload it with expected id
        file_for_test = self.get_files()[0]
        response = self.upload_file_for_test_to_file_storage(filename=file_for_test, tag=expected_tag)
        tag_from_response = response.json()['tag']
        Assertions.assert_json_value_by_name(response, 'tag', expected_tag,
                                             f" Unexpected tag: actual {tag_from_response}, expected:{expected_tag}")
        # delete file by expected name
        data = {'tag': expected_tag}
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

    @pytest.mark.parametrize('expected_mimetype', ['test1', 'test2', 'test3', 'test4', 'test5'])
    def test_delete_by_mimetype(self,expected_mimetype):
        # Prepare file for test then upload it with expected mimeType
        file_for_test = self.get_files()[0]
        response = self.upload_file_for_test_to_file_storage(filename=file_for_test,
                                                             mimetype=expected_mimetype)
        mimetype_from_response = response.json()['mimeType']
        Assertions.assert_json_value_by_name(response, 'mimeType', expected_mimetype,
                                             f" Unexpected tag: actual {mimetype_from_response}, expected:{expected_mimetype}")
        # delete file by expected mimeType
        data = {'mimeType': expected_mimetype}
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


    def test_delete_by_modification_time(self):
        # Prepare file for test then upload it with expected mimeType
        file_for_test = self.get_files()[0]
        response = self.upload_file_for_test_to_file_storage(filename=file_for_test)
        print(response.json())
        modification_time_from_response = response.json()['modificationTime']

        # delete file by expected mimeType
        data = {'modificationTime': modification_time_from_response}
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