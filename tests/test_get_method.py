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
            self.upload_file_for_delete_test(file=file)
        # get files without any params
        response = MyRequests.get('get')
        Assertions.base_assertions_for_get_method(response)
        files_from_response = response.json()
        amount_of_files_from_response = len(files_from_response)
        assert amount_of_files == amount_of_files_from_response, \
            f"Number of received files ({amount_of_files_from_response}) not equal number of  \
            sent files ({amount_of_files})"
