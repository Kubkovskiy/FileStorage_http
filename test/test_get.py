from test.client_for_test import Client
import requests
from unittest import TestCase
import json

clt = Client()


class TestGet(TestCase):
    upload_files = set()
    response_json = {"response": []}

    @staticmethod
    def upload_all_file_from_dir():
        f"""first of all past in {clt.FILES_TO_UPLOAD_PATH} some files"""
        result = []
        files = clt.files_in_folder()
        for file in files:
            # print(i)
            response = clt.post_params(file, tag='test')
            res = response.json()
            TestGet.upload_files.add(res['id'])
            result.append(response.json())
        return result
        # print(json.dumps(response, indent=4))

    @classmethod
    def setUpClass(cls) -> None:
        # file_list = clt.files_in_folder()
        TestGet.response_json['response'] = TestGet.upload_all_file_from_dir()

    @classmethod
    def tearDownClass(self) -> None:
        """ delete all uploaded files after test by id """
        clt.delete(tuple(TestGet.upload_files))

    def setUp(self) -> None:
        files = clt.files_in_folder()
        """check there are files in the folder"""
        self.assertNotEqual(len(files), 0, 'THERE ARE NO FILES TO UPLOAD TO THE FILE STORAGE')

    # def tearDown(self) -> None:
    #     """  Add file id to 'upload_files" for deleting after test """
    #     TestGet.upload_files.add(clt.get_id_from_response(clt.response))

    def test_get_without_params(self):
        clt.response = clt.get()
        st_code = clt.response.status_code
        self.assertEqual(st_code, 200, 'Wrong status_code')


