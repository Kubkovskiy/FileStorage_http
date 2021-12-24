import os
import requests
import json


def create_dir(path="files_to_upload") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'


PORT = 9000
URL = 'http://127.0.0.1:{}'.format(PORT)
FILES_TO_UPLOAD_PATH = create_dir('files_to_upload')
DOWNLOAD_PATH = create_dir('downloaded_files')


def get(file_id: (int, tuple) = None, name: str = None, tag: str = None, size: int = None):
    """Метод GET. Если без параметров- запрашивает все файлы.
    если параметру соответствует несколько значений - передавать в виде tuple"""
    params = {"name": name, "tag": tag, "id": file_id, "size": size}
    r = requests.get(URL + '/api/get', params=params)
    print(f"\n status code: {r.status_code} \n")
    try:
        print(json.dumps(r.json(), indent=4))
    except:
        pass
    return r


def post(filename, file_id: int = None, name: str = None, tag: str = None):
    """Method POST where params sent in data"""
    if not name:
        name = filename
    files = {"file": (name, open(FILES_TO_UPLOAD_PATH + filename, 'rb'))}
    payload = {"name": filename, "tag": tag, "id": file_id}
    r = requests.post(URL + '/api/upload', files=files, data=payload)
    print(f"\n status code: {r.status_code} \n")
    # print(json.dumps(r.json(), indent=4))
    try:
        print(json.dumps(r.json(), indent=4))
    except:
        print(r.text)
    return r


def post_params(filename, file_id: int = None, name: str = None, tag: str = None):
    """Method POST where params sent in params"""
    if name:
        filename = name
    # files = {"file": (filename, open(FILES_TO_UPLOAD_PATH + filename, 'rb'))}
    with open(FILES_TO_UPLOAD_PATH + filename, 'rb') as f:
        data = f.read()
        params = {"name": filename, "tag": tag, "id": file_id}
        r = requests.post(URL + '/api/upload', params=params, data=data)
        try:
            print(json.dumps(r.json(), indent=4))
        except:
            pass
        return r


def delete(file_id=None, name: str = None, tag: str = None, size: int = None, mime_type: str = None):
    """Method DELETE"""
    params = {"name": name, "tag": tag, "id": file_id, "mimeType": mime_type, 'size': size}
    r = requests.delete(URL + '/api/delete', params=params)
    # print(f"\n status code: {r.status_code}, {r.text} \n")
    print(r.text)
    # print(json.dumps(r.json(), indent=4))


def download(file_id: int):
    """Метод DOWNLOAD. принимает один параметр - id.
    если параметру соответствует несколько значений - передавать в виде tuple"""
    params = {"id": file_id}
    r = requests.get(URL + '/api/download', params=params)
    print(f"\n status code: {r.status_code} \n")
    if r.status_code == 200:
        try:
            filename = r.headers.get('Content-Disposition')[9:]
            with open(DOWNLOAD_PATH + filename, 'wb') as f:
                f.write(r.content)
                print(f'File {filename} downloaded successfully!')
                return r
        except:
            pass
    else:
        try:
            print(json.dumps(r.json(), indent=4))
        except:
            pass
