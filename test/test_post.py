from unittest import TestCase
from client_for_test import Client


class TestPost(TestCase):
    clt = Client()
    def setUp(self) -> None:
        files = self.clt.files_in_folder()
        self.assertNotEqual(len(files), 0, 'THERE ARE NO FILES TO UPLOAD TO THE FILE STORAGE')

    def test_post_with_params(self):
        self.response = self.clt.post_params('test1.doc')
        st_code = self.response.status_code
        self.assertEqual(st_code, 201, 'Wrong status_code')


    # def test_is_response_json(self):
    #         self.assertRaises()


    def test_post_multytape_form_data(self):
        response = self.clt.post('test1.doc')
        st_code = response.status_code
        self.assertEqual(st_code, 201, 'Wrong status_code')

