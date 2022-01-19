import datetime
import json
import os
import zipfile
import requests
from requests import Response
from lib.assertions import Assertions


class BaseCase:
    FILES_FOR_UPLOAD = 'tests/files_for_upload/'


    @staticmethod
    def get_header(response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with the name {header_name} \
                                                in response"
        return response.headers[header_name]
    @staticmethod
    def get_json_value(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format, Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def download_file_from_cloud(self, url: str):
        """Download file from yandex disk. return (content-type:str, headers:dict, file:bytes) """
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key='
        # Получаем загрузочную ссылку
        final_url = f"{base_url}{url}"
        response = requests.get(final_url)
        Assertions.assert_expected_status_code(response, 200)
        download_url = self.get_json_value(response, 'href')
        # Загружаем файл и возвращаем его
        download_response = requests.get(download_url)
        Assertions.assert_expected_status_code(download_response, 200)
        return download_response

    def download_and_extract_zip_archive_from_cloud(self, url: str, filename: str = None) -> list:
        """
        url - address to folder 'files_for_upload' on cloud. filename = test_+time_now.zip(default),
        path to upload_folder = 'tests/files_for_upload/
        First will download archive and save with 'filename' at 'path'\
        then extract 'files_for_upload' folder to 'tests/' dir
        after delete archive
        """
        content = self.download_file_from_cloud(url).content
        modification_time = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        # Check filename and path if None use defaut
        base_name = filename if filename else f'test_{modification_time}.zip'
        path_to_upload_folder = BaseCase.FILES_FOR_UPLOAD
        full_name = path_to_upload_folder + base_name
        # check is there 'tests/files_for_upload/ folder if not should create
        if not os.path.isdir(path_to_upload_folder):
            os.mkdir(path_to_upload_folder)
        assert os.path.isdir(path_to_upload_folder), f'There are not folder {path_to_upload_folder}'
        # check is file zip archive and extract it
        with open(full_name, 'wb') as f:
            f.write(content)
        assert zipfile.is_zipfile(full_name), f"Content from cloud isn't zip archive"
        with zipfile.ZipFile(full_name, 'r') as z:
            z.extractall('tests/')
        # remove archive
        os.remove(full_name)
        # return list with names of file
        names_list = os.listdir(path_to_upload_folder)
        # check is folder not empty
        assert len(names_list) > 0, f"Files_for_upload is empty"
        return names_list
