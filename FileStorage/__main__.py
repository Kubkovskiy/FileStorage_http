# FileStorage main file
from datetime import datetime
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from FileStorage_http.StorageDB.DBmethods import DBconnect
from methods import create_dir, generate_filename, check_name_in_params
import re
import uuid
import urllib

PORT = 9000
URL = '127.0.0.1'
UPLOADED_FILES_PATH = create_dir('uploaded_files')
db = DBconnect()


class MyAwesomeHandler(BaseHTTPRequestHandler):
    def write_response(self, code: int):
        self.send_response(code)
        self.end_headers()

    def do_GET(self):
        self.write_response(200)
        my_path = self.path
        self.wfile.write(my_path.encode())
        print(self.client_address)

    def do_POST(self):
        params = urllib.parse.parse_qs(self.path[2:])
        file_id = params['file_id'][0] if 'file_id' in params else db.return_next_id()
        filename = params['name'][0] if 'name' in params else file_id
        name, execution = os.path.splitext(filename)
        tag = params['tag'][0] if 'tag' in params else None
        size = int(self.headers['content-length'])
        content_type = self.headers.get_content_type()
        modification_time = str(datetime.now())

        # загрузка в ДБ, добавить  проверку по File_id
        data = {'id': file_id, 'name': name, 'tag': tag, 'mimeType': content_type,
                'size': size, 'modificationTime': modification_time}
        ad_to_db = db.add_to_db(data)

        # upload in dir
        if content_type == 'multipart/form-data':
            self.boundary = self.headers.get_boundary().encode()
            execution = self.get_execution()
            upload_info = self.save_file_to_dir(file_id, execution)
            print(upload_info, "by: ", self.client_address)
            return self.write_response(201), self.wfile.write(upload_info.encode())
        # if not 'multipart/form-data':
        else:
            file = self.rfile.read(size)
            with open(UPLOADED_FILES_PATH + file_id + execution, 'wb') as f:
                f.write(file)
                response = f"File '{name}'upload successfully!"
                print(response)
                return self.write_response(201), self.wfile.write(response.encode())

    def get_execution(self) -> str:
        """читает Content-Description построчно и возвращает дефолтное расширение"""
        line = self.rfile.readline()
        if self.boundary in line:
            line_with_filename = self.rfile.readline()
            filename = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"',
                                  line_with_filename.decode())[0]
            name, execution = os.path.splitext(filename)
            while len(line) > 2:
                line = self.rfile.readline()
            return execution

    def save_file_to_dir(self, file_id, execution):
        """save file at UPLOADED_FILES_PATH dir with self.filename"""
        try:
            out = open(UPLOADED_FILES_PATH + file_id + execution, 'wb')
        except IOError:
            return "Can't create file to write!!"
        else:
            with out:
                pre_line = self.rfile.readline()
                while True:
                    line = self.rfile.readline()
                    if self.boundary in line:
                        pre_line = pre_line[0:-1]
                        if pre_line.endswith(b'\r'):
                            pre_line = pre_line[0:-1]
                        out.write(pre_line)
                        break
                    else:
                        out.write(pre_line)
                        pre_line = line
        return f"File upload successfully"


def run():
    print('server started')
    server_address = (URL, PORT)
    server = HTTPServer(server_address, MyAwesomeHandler)
    server.serve_forever()


run()
