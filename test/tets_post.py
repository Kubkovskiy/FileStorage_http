import requests
import os
from settings import URL, UPLOAD_DIR, API_POST, post
import json

WRONG_API = ['/api/wrong']




class TestPOST:
    # def test_are_files_in_upload_dir(self):
    #     files = os.listdir(UPLOAD_DIR)
    #     print(files)
    #     print(os.getcwd())
    #     files_amount = len(files)
    #     assert files_amount > 0, 'No files in upload_directory'

    def test_post_all_files_in_dir_without_data(self):
        files = os.listdir(UPLOAD_DIR)
        for file in files:
            response = post(file)
            assert response.status_code == 201, "пока так"



#
#     print(f"\n status code: {response.status_code} \n")
#     print(json.dumps(response.json(), indent=4))

def post(file):
    """fot upload binary files"""
    with open(file, 'rb') as f:
        data = f.read()
        params = {'name': file, 'tag': 'txt1', "file_id": 123}
        r = requests.post(URL, data=data, params=params)
        print(r.text)

#
# def post_multy(file):
#     files = {'file': (file, open(file, 'rb'))}
#     params = {'name': file, 'tag': 'txt', "file_id": 1}
#     r = requests.post(URL, files=files, params=params)
#     print(r.text)
#
#
# # post_multy('1 Москва.xlsx')
# post('1 Москва.xlsx')
