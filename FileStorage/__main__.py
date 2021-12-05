# FileStorage main file
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
#
# from FileStorage_http.StorageDB.DBmethods import add_to_db
from methods import create_dir, generate_filename, check_name_in_params
import re
import uuid
import urllib

PORT = 9000
URL = '127.0.0.1'
UPLOADED_FILES_PATH = create_dir('uploaded_files')


def multipart_upload():
    pass


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
        self.params = urllib.parse.parse_qs(self.path[2:])
        self.tag = self.params['tag'][0] if 'tag' in self.params else None
        self.file_id = self.params['file_id'][0] if 'file_id' in self.params else uuid.uuid4().hex
        self.content_type = self.headers.get_content_type()
        self.size = int(self.headers['content-length'])

        # upload in dir
        if self.content_type == 'multipart/form-data':
            self.boundary = self.headers.get_boundary().encode()
            self.execution = self.get_execution()
            if check_name_in_params(self.params):
                name = self.params['name'][0]
                self.name, _ = os.path.splitext(name)
            else:
                self.name = self.file_id
            self.params = {'tag': self.tag, 'file_id': self.file_id,
                           'content_type': self.content_type, 'size': self.size, 'name': self.name}
            upload_info = self.save_file_to_dir()
            print(upload_info, "by: ", self.client_address)
            return self.write_response(201), self.params, self.wfile.write(upload_info.encode())
        else:  # if not 'multipart/form-data':
            if check_name_in_params(self.params):
                name = self.params['name'][0]
                self.name, self.execution = os.path.splitext(name)
            else:
                self.name, self.execution = os.path.splitext(self.file_id)
            self.file = self.rfile.read(self.size)
            self.params = {'tag': self.tag, 'file_id': self.file_id,
                           'content_type': self.content_type, 'size': self.size, 'name': self.name}
            with open(UPLOADED_FILES_PATH + self.name + self.execution, 'wb') as f:
                f.write(self.file)
                return self.write_response(201), self.wfile.write\
                    (f"File '{self.name}'upload success!".encode())

    def get_execution(self) -> str:
        """читает Content-Description построчно и возвращает дефолтное расширение"""
        self.boundary = self.headers.get_boundary().encode()
        self.discription_size = 0
        self.line = self.rfile.readline()
        self.discription_size += len(self.line)
        if self.boundary in self.line:
            line_with_filename = self.rfile.readline()
            self.discription_size += len(line_with_filename)
            filename = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"',
                                       line_with_filename.decode())[0]
            name, execution = os.path.splitext(filename)
            while len(self.line) > 2:
                self.line = self.rfile.readline()
                self.discription_size += len(self.line)
            return execution

    def save_file_to_dir(self):
        """save file at UPLOADED_FILES_PATH dir with self.filename"""
        try:
            out = open(UPLOADED_FILES_PATH + self.name + self.execution, 'wb')
        except IOError:
            return "Can't create file to write!!"
        else:
            with out:
                pre_line = self.rfile.readline()
                while True:
                    self.line = self.rfile.readline()
                    if self.boundary in self.line:
                        pre_line = pre_line[0:-1]
                        if pre_line.endswith(b'\r'):
                            pre_line = pre_line[0:-1]
                        out.write(pre_line)
                        break
                    else:
                        out.write(pre_line)
                        pre_line = self.line
        return f"File '{self.name}' upload success"


def run():
    print('server started')
    server_address = (URL, PORT)
    server = HTTPServer(server_address, MyAwesomeHandler)
    server.serve_forever()


run()
