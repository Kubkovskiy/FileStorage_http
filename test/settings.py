import os
import requests


def create_dir(dir) -> str:
    try:
        os.mkdir(dir)
        return os.getcwd() + '\\'+ dir
    except FileExistsError:
        return os.getcwd() + '\\'+ dir



PORT = 9000
URL = 'http://127.0.0.1:{}'.format(PORT)
UPLOAD_DIR = create_dir('files_to_upload')
API_GET = '/api/get'
API_POST = '/api/upload'
API_DELETE = '/api/delete'
API_DOWNLOAD = '/api/download'


def get(url=URL, api=API_POST, file_id: (int, tuple) = None, name: str = None, tag: str = None, size: int = None):
    """Метод GET. Если без параметров- запрашивает все файлы.
    если параметру соответсвует несколько значений - передавать в виде tuple"""
    params = {"name": name, "tag": tag, "id": file_id, "size": size}
    request = requests.get(url+api, params=params)

    return request


def post(filename, url=URL, api=API_POST, file_id: int = None, name: str = None, tag: str = None):
    """Method POST"""
    if name:
        filename = name
    files = {"file": (filename, open(UPLOAD_DIR + filename, 'rb'))}
    payload = {"name": filename, "tag": tag, "id": file_id}
    response = requests.post(url + api, files=files, data=payload)
    return response

    # print(f"\n status code: {r.status_code} \n")
    # print(json.dumps(r.json(), indent=4))