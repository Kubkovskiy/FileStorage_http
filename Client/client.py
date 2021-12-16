import os
import requests


def create_dir(path="files_to_upload") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'


PORT = 9000
URL = 'http://127.0.0.1:{}'.format(PORT)
FILES_TO_UPLOAD_PATH = create_dir('files_to_upload')

def get(file_id: int = None, name: str = None, tag: str = None, size:int = None):
    params = {'name': name, 'tag': tag, "id": file_id, "size": size}
    r = requests.get(URL+'/api/get', params=params)
    print(r.text)


def post(filename, file_id: int = None, name: str = None, tag: str = None):
    """Method POST"""
    if name:
        filename = name
    files = {'file': (filename, open(FILES_TO_UPLOAD_PATH + filename, 'rb'))}
    payload = {"name": filename, "tag": tag, "id": file_id}
    r = requests.post(URL + '/api/upload', files=files, data=payload)
    print(r.status_code, r.json(), sep='\n')


get(file_id=124, size=549)

# post('все опоры.txt')

