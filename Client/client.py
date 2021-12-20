import os
import requests
import json




def create_dir(self, path="files_to_upload") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'


PORT = 9000
URL = 'http://127.0.0.1:{}'.format(PORT)
FILES_TO_UPLOAD_PATH = create_dir('files_to_upload')


def get(file_id: (int, tuple) = None, name: str = None, tag: str = None, size: int = None):
    """Метод GET. Если без параметров- запрашивает все файлы.
    если параметру соответсвует несколько значений - передавать в виде tuple"""
    params = {"name": name, "tag": tag, "id": file_id, "size": size}
    r = requests.get(URL+'/api/get', params=params)
    print(f"\n status code: {r.status_code} \n")
    print(json.dumps(r.json(), indent=4))
    return r

def post(filename, file_id: int = None, name: str = None, tag: str = None):
    """Method POST"""
    if name:
        filename = name
    files = {"file": (filename, open(FILES_TO_UPLOAD_PATH + filename, 'rb'))}
    payload = {"name": filename, "tag": tag, "id": file_id}
    r = requests.post(URL + '/api/upload', files=files, data=payload)
    print(f"\n status code: {r.status_code} \n")
    print(json.dumps(r.json(), indent=4))


# get(size=26186)
# get(file_id=(1, 2, 3), size=549)

# post('все опоры.txt')
# post('file_storage_good.zip')
# post('1 Москва.xlsx')

