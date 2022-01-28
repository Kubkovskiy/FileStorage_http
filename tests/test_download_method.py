import os
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestGetMethod(BaseCase):
    @classmethod
    def setup_class(cls):
        print('\n Start TestDownloadMethod \n')
        # delete files from FileStorage
        cls.delete_all_files_from_server()

    @classmethod
    def teardown_class(cls):
        # delete files from FileStorage
        cls.delete_all_files_from_server()
        # delete tests/files_for_upload/
        cls.delete_upload_files()
        print('\n Finish TestDownloadMethod')

    def test_download_by_id(self):
        # upload files to FileStorage
        file_id = 1
        filename = "test_for_download"
        file = self.get_files()[0]
        upload_file_size = os.path.getsize(BaseCase.FILES_FOR_UPLOAD + file)
        response_post = self.upload_file_for_test_to_file_storage(file, file_id=file_id, name=filename, mimetype='auto')
        file_weight = response_post.json()['size']
        # download files by id
        response = MyRequests.get('download', params={'id': file_id})
        Assertions.assert_expected_status_code(response, 200)
        content = response.content
        assert isinstance(content, bytes), "Response not contains bytes onj"
        headers_dict = response.headers
        assert 'Content-Disposition' in headers_dict, "Headers not contain 'Content-Disposition"
        filename_from_server = headers_dict['Content-Disposition'].replace('filename=', '')
        with open(BaseCase.FILES_FOR_UPLOAD + filename_from_server, 'wb') as f:
            f.write(content)
        assert filename_from_server in os.listdir(BaseCase.FILES_FOR_UPLOAD), \
            f"There is not file {filename_from_server} in {BaseCase.FILES_FOR_UPLOAD}"
        download_file_size = os.path.getsize(BaseCase.FILES_FOR_UPLOAD + filename_from_server)
        assert upload_file_size == download_file_size, \
            f"Size of the uploaded file {upload_file_size} " \
            f"is not equal to size of the downloaded file {download_file_size}"
