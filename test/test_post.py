from unittest import TestCase
from test.client_for_test import Client

clt = Client()


class TestPost(TestCase):
    """Tests for upload where parameters are passed in the query string"""
    upload_files = set()

    @classmethod
    def tearDownClass(self) -> None:
        """ delete all uploaded files after test by id """
        clt.delete(tuple(TestPost.upload_files))

    def setUp(self) -> None:
        """check there are files in the folder"""
        files = clt.files_in_folder()
        self.assertNotEqual(len(files), 0, 'THERE ARE NO FILES TO UPLOAD TO THE FILE STORAGE')

    def tearDown(self) -> None:
        """  Add file id to 'upload_files" for deleting after test """
        TestPost.upload_files.add(clt.get_id_from_response(clt.response))

    def test_post_without_params(self):
        """ Upload file without parameters """
        clt.response = clt.post_params('test1.doc')
        st_code = clt.response.status_code
        self.assertEqual(st_code, 201, 'Wrong status_code')

    def test_post_with_params(self):
        """ Upload file with parameters id, name, tag"""
        file_id, name, tag = 111, 'test.doc', 'test'
        clt.response = clt.post_params('test1.doc', name=name, tag=tag, file_id=file_id)
        st_code = clt.response.status_code
        self.assertEqual(st_code, 201, 'Wrong status_code')

    def test_is_response_json(self):
        """ Check is response contain JSON """
        clt.response = clt.post_params('test1.doc')
        self.assertIsInstance(clt.response.json(), dict, "THERE ISN'T JSON IN RESPONSE")

    def test_is_response_body_right(self):
        """ Check is response contain correct data (id,name,tag,size,mimeType,modificationTime) """
        file_id, name, tag = 111, 'test.doc', 'test'
        clt.response = clt.post_params('test1.doc', name=name, tag=tag, file_id=file_id)
        response_body = clt.response.json()
        self.assertEqual(int(response_body['id']), file_id, 'Wrong id')
        self.assertTrue(response_body['name'] in name, 'Wrong name')
        self.assertEqual(response_body['tag'], tag, 'Wrong tag')


class TestPostFormData(TestCase):
    """Tests for upload where parameters are passed in the request body"""
    upload_files = set()

    @classmethod
    def tearDownClass(self) -> None:
        """ delete all uploaded files after test by id """
        clt.delete(tuple(TestPost.upload_files))

    def setUp(self) -> None:
        files = clt.files_in_folder()
        """check that there are files in the folder"""
        self.assertNotEqual(len(files), 0, 'THERE ARE NO FILES TO UPLOAD TO THE FILE STORAGE')

    def tearDown(self) -> None:
        """  Add file id to 'upload_files" for deleting after test """
        TestPost.upload_files.add(clt.get_id_from_response(clt.response))

    def test_post_without_data(self):
        """ Upload file without parameters """
        clt.response = clt.post_form_data('test1.doc')
        st_code = clt.response.status_code
        self.assertEqual(st_code, 201, 'Wrong status_code')

    def test_post_with_data(self):
        """ Upload file with parameters id, name, tag"""
        file_id, name, tag = 111, 'test.doc', 'test'
        clt.response = clt.post_form_data('test1.doc', file_id=file_id, name=name, tag=tag)
        st_code = clt.response.status_code
        self.assertEqual(st_code, 201, 'Wrong status_code')

    def test_is_response_json(self):
        """ Check is response contain JSON """
        clt.response = clt.post_form_data('test1.doc')
        self.assertIsInstance(clt.response.json(), dict, "THERE ISN'T JSON IN RESPONSE")

    def test_is_response_body_right(self):
        """ Check is response contain correct data (id,name,tag,size,mimeType,modificationTime) """
        file_id, name, tag = 111, 'test.doc', 'test'
        clt.response = clt.post_form_data('test1.doc', name=name, tag=tag, file_id=file_id)
        response_body = clt.response.json()
        self.assertEqual(int(response_body['id']), file_id, 'Wrong id')
        self.assertTrue(response_body['name'] in name, 'Wrong name')
        self.assertEqual(response_body['tag'], tag, 'Wrong tag')
