import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestGetMethod(BaseCase):

    def setup_class(cls):
        print('\n Start TestGetMethod \n')
        # delete files from FileStorage
        response = cls.delete_all_files_from_server()

    def teardown_class(cls):
        # delete files from FileStorage
        cls.delete_all_files_from_server()
        # delete tests/files_for_upload/
        cls.delete_upload_files()
        print('\n Finish TestGetMethod')

    def test_get_without_params(self):
        # get files from cloud
        files_for_test = self.get_files()
        amount_of_files = len(files_for_test)
        # upload files to FileStorage
        for file in files_for_test:
            self.upload_file_for_test_to_file_storage(filename=file)
        # get files without any params
        response = MyRequests.get('get')
        Assertions.base_assertions_for_positive_get_method(response)
        files_from_response = response.json()
        amount_of_files_from_response = len(files_from_response)
        assert amount_of_files == amount_of_files_from_response, \
            f"Number of received files ({amount_of_files_from_response}) not equal number of  \
            sent files ({amount_of_files})"

    def test_get_with_id(self):
        # upload file with file_id
        files_for_test = self.get_files()
        list_id = [10, 20, 30, 40, 50]
        for i in range(len(files_for_test)):
            file = files_for_test[i]
            file_dict = self.open_file_from_upload_folder(file)
            file_id = list_id[i]
            data, headers, payload = self.set_data_to_post_method(file_dict, file_id=file_id)
            response_post = MyRequests.post("upload", data, headers, payload)
            Assertions.base_assertions_for_positive_post_method(response_post)
        # test get
        expected_id = []
        data = {"id": expected_id}
        count = 0
        for file_id in list_id:
            expected_id.append(file_id)
            count += 1
            response = MyRequests.get('get', params=data)
            response_list = response.json()
            Assertions.base_assertions_for_positive_get_method(response)
            num_of_files = len(response_list)
            assert num_of_files == count, \
                f"Number of files received ({num_of_files}) is not equal to the expected number ({count})"
            received_id = []
            for meta in response_list:
                received_id.append(meta['id'])
            assert expected_id == received_id, \
                f"Unexpected id! expected - {expected_id}, actual - {received_id}"

    def test_get_with_name(self):
        # upload file with file_id
        files_for_test = self.get_files()
        list_name = ['test1', 'test2', 'test3', 'test4', 'test5']
        for i in range(len(files_for_test)):
            file = files_for_test[i]
            file_dict = self.open_file_from_upload_folder(file)
            name = list_name[i]
            data, headers, payload = self.set_data_to_post_method(file_dict, name=name)
            response_post = MyRequests.post("upload", data, headers, payload)
            Assertions.base_assertions_for_positive_post_method(response_post)
        # test get
        expected_name = []
        data = {"name": expected_name}
        count = 0
        for name in list_name:
            expected_name.append(name)
            count += 1
            response = MyRequests.get('get', params=data)
            response_list = response.json()
            Assertions.base_assertions_for_positive_get_method(response)
            num_of_files = len(response_list)
            assert num_of_files == count, \
                f"Number of files received ({num_of_files}) is not equal to the expected number ({count})"
            received_name = []
            for meta in response_list:
                received_name.append(meta['name'])
            assert expected_name == received_name, \
                f"Unexpected name! expected - {expected_name}, actual - {received_name}"

    def test_get_with_tag(self):
        # upload file with file_id
        files_for_test = self.get_files()
        list_tag = ['test1', 'test2', 'test3', 'test4', 'test5']
        for i in range(len(files_for_test)):
            file = files_for_test[i]
            file_dict = self.open_file_from_upload_folder(file)
            tag = list_tag[i]
            data, headers, payload = self.set_data_to_post_method(file_dict, tag=tag)
            response_post = MyRequests.post("upload", data, headers, payload)
            Assertions.base_assertions_for_positive_post_method(response_post)
        # test get
        expected_tag = []
        data = {"tag": expected_tag}
        count = 0
        for tag in list_tag:
            expected_tag.append(tag)
            count += 1
            response = MyRequests.get('get', params=data)
            response_list = response.json()
            Assertions.base_assertions_for_positive_get_method(response)
            num_of_files = len(response_list)
            assert num_of_files == count, \
                f"Number of files received ({num_of_files}) is not equal to the expected number ({count})"
            received_tag = []
            for meta in response_list:
                received_tag.append(meta['tag'])
            assert expected_tag == received_tag, \
                f"Unexpected tag! expected - {expected_tag}, actual - {received_tag}"

    def test_get_with_mimetype(self):
        # upload file with file_id
        files_for_test = self.get_files()
        list_mimetype = ['test1', 'test2', 'test3', 'test4', 'test5']
        for i in range(len(files_for_test)):
            file = files_for_test[i]
            file_dict = self.open_file_from_upload_folder(file)
            mimetype = list_mimetype[i]
            data, headers, payload = self.set_data_to_post_method(file_dict, content_type=mimetype)
            response_post = MyRequests.post("upload", data, headers, payload)
            Assertions.base_assertions_for_positive_post_method(response_post)
        # test get
        expected_mimetype = []
        data = {"mimeType": expected_mimetype}
        count = 0
        for mimetype in list_mimetype:
            expected_mimetype.append(mimetype)
            count += 1
            response = MyRequests.get('get', params=data)
            response_list = response.json()
            Assertions.base_assertions_for_positive_get_method(response)
            num_of_files = len(response_list)
            assert num_of_files == count, \
                f"Number of files received ({num_of_files}) is not equal to the expected number ({count})"
            received_mimetype = []
            for meta in response_list:
                received_mimetype.append(meta['mimeType'])
            assert expected_mimetype == received_mimetype, \
                f"Unexpected mimetype! expected - {expected_mimetype}, actual - {received_mimetype}"