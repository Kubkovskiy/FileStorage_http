import os
import requests
import json


def create_dir(dir_name="files_to_upload") -> str:
    f"""check is there dir {dir_name}. and create if it's not"""
    full_path = os.getcwd()
    if os.path.basename(full_path) != 'test':
        os.chdir('test')
    """check is dir created."""
    if dir_name in os.listdir():
        return dir_name + '/'
    os.mkdir(dir_name)
    return dir_name + '/'


class Client:
    def __init__(self):
        self.PORT = 9000
        self.URL = 'http://127.0.0.1:{}'.format(self.PORT)
        self.FILES_TO_UPLOAD_PATH = create_dir('files_to_upload')
        self.DOWNLOAD_PATH = create_dir('downloaded_files')
        self.API_GET = '/api/get'
        self.API_POST = '/api/upload'
        self.API_DELETE = '/api/delete'
        self.API_DOWNLOAD = '/api/download'
        self.response = None


    def get(self, file_id: (int, tuple) = None, name: (str, tuple) = None,
            tag: (str, tuple) = None, size: (int, tuple) = None):
        """Метод GET. Если без параметров- запрашивает все файлы.
        если параметру соответствует несколько значений - передавать в виде tuple"""
        params = {"name": name, "tag": tag, "id": file_id, "size": size}
        response = requests.get(self.URL + self.API_GET, params=params)
        return response


    def post_form_data(self, filename, file_id: int = None, name: str = None, tag: str = None):
        """Method POST where params sent in data"""
        if not name:
            name = filename
        files = {"file": (name, open(self.FILES_TO_UPLOAD_PATH + filename, 'rb'))}
        payload = {"name": filename, "tag": tag, "id": file_id}
        r = requests.post(self.URL + self.API_POST, files=files, data=payload)
        return r


    def post_params(self, filename, file_id: int = None, name: str = None, tag: str = None):
        """Method POST where params sent in params"""
        if not name:
            name = filename
        with open(self.FILES_TO_UPLOAD_PATH + filename, 'rb') as f:
            data = f.read()
            params = {"name": name, "tag": tag, "id": file_id}
            r = requests.post(self.URL + self.API_POST, params=params, data=data)
            return r


    def upload_all_files_from_dir(self):
        file_list = os.listdir()
        return file_list


    def delete(self, file_id=None, name: str = None, tag: str = None, size: int = None, mime_type: str = None):
        """Method DELETE"""
        params = {"name": name, "tag": tag, "id": file_id, "mimeType": mime_type, 'size': size}
        r = requests.delete(self.URL + self.API_DELETE, params=params)


    def download(self,file_id: int):
        """Метод DOWNLOAD. принимает один параметр - id.
        если параметру соответствует несколько значений - передавать в виде tuple"""
        params = {"id": file_id}
        r = requests.get(self.URL + self.API_DOWNLOAD, params=params)
        print(f"\n status code: {r.status_code} \n")
        if r.status_code == 200:
            try:
                filename = r.headers.get('Content-Disposition')[9:]
                with open(self.DOWNLOAD_PATH + filename, 'wb') as f:
                    f.write(r.content)
                    print(f'File {filename} downloaded successfully!')
                    return r
            except:
                print('ERROR SAVING FILE')


    @staticmethod
    def print_json(response):
        try:
            print(json.dumps(response.json(), indent=4))
        except:
            print('=== The response not contains json ===')
            print(response.text)


    @staticmethod
    def get_id_from_response(response):
        return response.json()['id']


    def files_in_folder(self):
        my_dir = os.scandir(self.FILES_TO_UPLOAD_PATH)
        files = [i.name for i in my_dir]
        return files




    def delete_all(self):
        response = self.get()
        if response.status_code == 200:
            for i in response.json():
                self.delete(i['id'])


a = Client()