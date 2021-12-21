import requests
import os
from settings import URL, UPLOAD_DIR, API_GET, get
import json

WRONG_API = ['/api/wrong']


class TestGET:
    def test_get_without_params(self):
        response = get()
        assert response.status_code == 200, "unexpected status code."

    def test_post_all_files_in_dir_without_data(self):
        files = os.listdir(UPLOAD_DIR)
        for file in files:
            response = post(file)
            assert response.status_code == 201, "пока так"



#