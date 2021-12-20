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
    def write_response(self, code: int, payload: any = None):
        self.send_response(code)
        self.end_headers()
        if payload:
            if isinstance(payload, (bytes, int)):
                self.wfile.write(payload)
            elif isinstance(payload, (str)):
                self.wfile.write(payload.encode())
            else:
                raise TypeError('pass')

    def do_GET(self):
        if '/api/get' != urlparse(self.path).path:
            return self.write_response(404), self.wfile.write(b"404 Not Found")
        query = parse_qs(urlparse(self.path).query)
        result = db.parse_from_db(query)
        result_json = json.dumps(result).encode()
        if len(result) == 0:
            message = b"{'message': 'No results =('}"
            return self.write_response(400, message)
        return self.write_response(200, result_json)

    def do_POST(self):
        if self.path != '/api/upload':
            message = b"{'message': '404 Not Found'}"
            return self.write_response(404, message)

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
        return self.write_response(201, result)


def runserver():
    try:
        print('http server is starting...')
        server_address = (URL, PORT)
        server = HTTPServer(server_address, MyAwesomeHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


def stopserver():
    server_address = (URL, PORT)
    server = HTTPServer(server_address, MyAwesomeHandler)
    server.server_close()


if __name__ == '__main__':
    runserver()
