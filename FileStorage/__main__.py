# FileStorage main file
from datetime import datetime
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from FileStorage_http.StorageDB.DBmethods import DBconnect
from methods import create_dir
from urllib.parse import urlparse, parse_qs
import cgi

PORT = 9000
URL = '127.0.0.1'
UPLOADED_FILES_PATH = create_dir('uploaded_files')
db = DBconnect()


class MyAwesomeHandler(BaseHTTPRequestHandler):
    def write_response(self, code: int):
        self.send_response(code)
        self.end_headers()

    def do_GET(self):
        if '/api/get' != urlparse(self.path).path:
            return self.write_response(404), self.wfile.write(b"404 Not Found")
        query = parse_qs(urlparse(self.path).query)
        result = db.parse_from_db(query)
        result1 = json.dumps(result)
        self.write_response(200), self.wfile.write(result1.encode())

        print(self.client_address)

    def do_POST(self):
        if self.path != '/api/upload':
            return self.write_response(404), self.wfile.write(b"404 Not Found")

        params = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                  environ={'REQUEST_METHOD': 'POST'})
        file = params.getvalue('file')
        file_id = params.getvalue('id') if 'id' in params else db.return_next_id()
        filename = params['file'].filename
        name, execution = os.path.splitext(filename)
        name = os.path.splitext(filename)[0] if 'name' in params else file_id
        tag = params.getvalue('tag') if 'tag' in params else None
        size = int(self.headers['content-length'])
        content_type = self.headers.get_content_type()
        modification_time = str(datetime.now())

        # загрузка в ДБ
        data = {'id': file_id, 'name': name, 'tag': tag, 'size': size, 'mimeType': content_type,
                'modificationTime': modification_time}
        result = json.dumps(db.add_to_db(data))
        # upload in dir
        with open(UPLOADED_FILES_PATH + file_id + execution, 'wb') as f:
            f.write(file)
            response = f"File '{name}'upload successfully!"
            print(response)
        return self.write_response(201), self.wfile.write(result.encode())


def run():
    print('server started')
    server_address = (URL, PORT)
    server = HTTPServer(server_address, MyAwesomeHandler)
    server.serve_forever()


run()
