import datetime
import json
import os
import zipfile
import requests
from requests import Response
from lib.assertions import Assertions
import magic


class BaseCase:
    FILES_FOR_UPLOAD = 'tests/files_for_upload/'
    URL_TO_ARCHIVE = "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"
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

    @staticmethod
    def download_file_from_cloud(url: str):
        """Download file from yandex disk. return (content-type:str, headers:dict, file:bytes) """
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key='
        # Получаем загрузочную ссылку
        final_url = f"{base_url}{url}"
        response = requests.get(final_url)
        Assertions.assert_expected_status_code(response, 200)
        download_url = BaseCase.get_json_value(response, 'href')
        # Загружаем файл и возвращаем его
        download_response = requests.get(download_url)
        Assertions.assert_expected_status_code(download_response, 200)
        return download_response

    @staticmethod
    def change_dir_to_root():
        """check current directory, if call not from root folder - change dir while not root."""
        curdir = os.getcwd().split('\\')
        while curdir[-1] != 'FileStorage_http':
            os.chdir('..')
            curdir = os.getcwd().split('\\')

    @staticmethod
    def download_and_extract_zip_archive_from_cloud(url: str, filename: str = None) -> list:
        """
        url - address to folder 'files_for_upload' on cloud. filename = test_+time_now.zip(default),
        path to upload_folder = 'tests/files_for_upload/
        First will download archive and save with 'filename' at 'path'\
        then extract 'files_for_upload' folder to 'tests/' dir
        after delete archive
        """
        content = BaseCase.download_file_from_cloud(url).content
        modification_time = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        # Check filename and path if None use defaut
        base_name = filename if filename else f'test_{modification_time}.zip'
        BaseCase.change_dir_to_root()
        path_to_upload_folder = BaseCase.FILES_FOR_UPLOAD
        full_name = path_to_upload_folder + base_name
        # check is there 'tests/files_for_upload/ folder? if not should create
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

    @staticmethod
    def check_upload_folder(name: str):
        """check upload folder and open file. return dict {filename: file(bytes)"""
        BaseCase.change_dir_to_root()
        path_to_upload_folder = BaseCase.FILES_FOR_UPLOAD
        assert os.path.isdir(path_to_upload_folder), f'There are not folder {BaseCase.FILES_FOR_UPLOAD}'
        assert os.path.isfile(BaseCase.FILES_FOR_UPLOAD + name), f'There are not file {name} in upload folder'

    @staticmethod
    def open_file_from_upload_folder(name: str) -> dict:
        """check upload folder and open file. return dict {filename: file(bytes)"""
        BaseCase.check_upload_folder(name)
        with open(BaseCase.FILES_FOR_UPLOAD + name, 'rb') as file:
            data = file.read()
            return {"content": data, "name": name}

    @staticmethod
    def set_data_to_post_method(file_dict: dict, file_id: int = None, name: str = None,
                                tag: str = None, content_type: str = None):
        """ Filling data to post method (files, headers, content-disposition)
        if content-type == auto : return c.type from 'python-magic', """
        # For auto MIME types
        if content_type == 'auto':
            ctype = magic.Magic(mime=True)
            content_type = ctype.from_file(BaseCase.FILES_FOR_UPLOAD + file_dict["name"])
        elif content_type:
            content_type = content_type
        headers = {"Content-Disposition": f"attachment; filename={file_dict['name']}"}
        payload = {"file": file_dict['content']}
        data = {"id": file_id, "name": name, "tag": tag, "content-type": content_type}
        return data, headers, payload

    @staticmethod
    def get_files():
        folder_path = BaseCase.FILES_FOR_UPLOAD
        if os.path.isdir(folder_path) and len(os.listdir(folder_path)) > 0:
            return os.listdir(folder_path)
        files = BaseCase.download_and_extract_zip_archive_from_cloud(BaseCase.URL_TO_ARCHIVE)
        return files
