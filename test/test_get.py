from test.client_for_test import Client
import requests
from unittest import TestCase

clt = Client()


class TestGet(TestCase):
    upload_files = set()
    response = []

    @staticmethod
    def upload_all_file_from_dir():
        f"""first of all past in {clt.FILES_TO_UPLOAD_PATH} some files"""
        result = []

        files = clt.files_in_folder()
        count = 1
        for file in files:
            name = 'test_name' + str(count)
            file_id = 0 + count
            response = clt.post_params(file, name=name, tag='test', file_id=file_id)
            res = response.json()
            TestGet.upload_files.add(res['id'])
            result.append(response.json())
            count += 1
        return result

    @classmethod
    def setUpClass(cls) -> None:
        """ deleting all from File Storage and then upload all files from folder
        save response in self.response"""
        clt.delete_all()
        TestGet.response = TestGet.upload_all_file_from_dir()

    @classmethod
    def tearDownClass(cls) -> None:
        """ delete all uploaded files after test by id """
        clt.delete(tuple(TestGet.upload_files))

    def setUp(self) -> None:
        files = clt.files_in_folder()
        """check there are files in the folder"""
        self.assertNotEqual(len(files), 0, 'THERE ARE NO FILES TO UPLOAD TO THE FILE STORAGE')

    def test_get_without_params(self):
        """should return all data"""
        clt.response = clt.get()
        st_code = clt.response.status_code
        self.assertEqual(st_code, 200, 'Wrong status_code')
        self.assertEqual(clt.response.json(), self.response, 'POST and GET data not equal')

    def test_get_with_id(self):
        file_id = (1, 3, 5)
        clt.response = clt.get(file_id=file_id)
        st_code = clt.response.status_code
        need_to_be = []
        self.assertEqual(st_code, 200, 'Wrong status_code')
        self.assertEqual(len(clt.response.json()), len(file_id),
                         f"amount of returning set data should be equal {len(file_id)} ")
        for i in self.response:
            if i["id"] in file_id:
                need_to_be.append(i)
        self.assertEqual(clt.response.json(), need_to_be, "Wrong response body")

    def test_get_with_name(self):
        name = ('test_name1', "test_name3", "test_name5")
        clt.response = clt.get(name=name)
        st_code = clt.response.status_code
        need_to_be = []
        self.assertEqual(st_code, 200, 'Wrong status_code')
        self.assertEqual(len(clt.response.json()), len(name),
                         f"amount of returning set data should be equal {len(name)} ")
        for i in self.response:
            if i["name"] in name:
                need_to_be.append(i)
        self.assertEqual(clt.response.json(), need_to_be, "Wrong response body")

    def test_get_with_tag(self):
        """should return all data with current tag"""
        tag = 'test'
        clt.response = clt.get(tag=tag)
        st_code = clt.response.status_code
        self.assertEqual(st_code, 200, 'Wrong status_code')
        self.assertEqual(clt.response.json(), self.response, 'POST and GET data not equal')

    def test_get_with_all_parameters(self):
        target = self.response[3]
        clt.response = requests.get(clt.URL + clt.API_GET, params=target)
        self.assertEqual(target, clt.response.json()[0], 'POST and GET data not equal')
