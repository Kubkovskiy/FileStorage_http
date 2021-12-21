# FileStorage main file
from datetime import datetime
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from StorageDB.DBmethods import DBconnect
from methods import create_dir
from urllib.parse import urlparse, parse_qs
import cgi

PORT = 9000
URL = '127.0.0.1'
UPLOADED_FILES_PATH = create_dir('uploaded_files')
db = DBconnect()


def delete_from_dir(result: [dict]) -> int:
    """take dict, deleting by file_id. return amount of deleted files"""
    count = len(result)
    for i in result:
        name_from_db = str(i['id'])
        for file in os.scandir(UPLOADED_FILES_PATH):
            name, execution = os.path.splitext(file.name)
            if name == name_from_db:
                os.remove(file.path)
                print(f"{file.name} was deleted successfully")
                break
    return count


class MyAwesomeHandler(BaseHTTPRequestHandler):
    def write_response(self, code: int, payload: any = None):
        self.send_response(code)
        self.end_headers()
        if payload:
            if isinstance(payload, (bytes, int)):
                self.wfile.write(payload)
            elif isinstance(payload, str):
                self.wfile.write(payload.encode())
            else:
                raise TypeError('pass')

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if not self.path_valid():
            return self.write_response(404, b"404 Not Found")
        result = db.parse_from_db(query)
        result_json = json.dumps(result).encode()
        if len(result) == 0:
            message = b'{"message": "No results =("}'
            return self.write_response(400, message)
        return self.write_response(200, result_json)

    def do_POST(self):

        if not self.path_valid():
            message = b"{'message': '404 Not Found'}"
            return self.write_response(404, message)
        size = int(self.headers['content-length'])
        content_type = self.headers.get_content_type()
        modification_time = str(datetime.now())

        if content_type in ['multipart/form-data', 'application/x-www-form-urlencoded']:
            params = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                      environ={'REQUEST_METHOD': 'POST'})
            file = params.getvalue('file')
            file_id = params.getvalue('id') if 'id' in params else db.return_next_id()
            filename = params['file'].filename
            name, execution = os.path.splitext(filename)
            name = os.path.splitext(filename)[0] if 'name' in params else file_id
            tag = params.getvalue('tag') if 'tag' in params else None

        else:
            params = parse_qs(urlparse(self.path).query)
            file = self.rfile.read(size)
            file_id = params['file_id'][0] if 'file_id' in params else db.return_next_id()
            filename = params['name'][0] if 'name' in params else file_id
            name, execution = os.path.splitext(filename)
            tag = params['tag'][0] if 'tag' in params else None

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

    def do_DELETE(self):
        if not self.path_valid():
            return self.write_response(404, b'{"message": "404 Not Found"}')
        query = parse_qs(urlparse(self.path).query)
        # if len(query) == 0:
        #     message = b'{"message": "bad request =(, write any parameters"}'
        #     return self.write_response(400, message)
        result = db.delete_from_db(query)
        if not result:
            return self.write_response(400, b'{"message": "No results =("}')
        amount_del_files = delete_from_dir(result)
        message = f'{amount_del_files} files deleted'
        return self.write_response(200, message.encode())


    def path_valid(self):
        valid_api = ['/api/get', '/api/upload', '/api/delete', '/api/download']
        query = parse_qs(urlparse(self.path).query)
        if query:
            index_questionMark = self.path.find('?')
            my_path = self.path[:index_questionMark]
            return my_path in valid_api
        return self.path in valid_api






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
