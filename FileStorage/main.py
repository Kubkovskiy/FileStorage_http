# FileStorage main file
from datetime import datetime
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from FileStorage.DBmethods import DBconnect
from methods import get_name_from_file_id, query_not_valid, path_not_valid, delete_from_dir, UPLOADED_FILES_PATH
from urllib.parse import urlparse, parse_qs
import cgi

PORT = 9000
URL = '127.0.0.1'

db = DBconnect()


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

    def parse_query(self):
        """parse query and check is query valid"""
        query = parse_qs(urlparse(self.path).query)
        if query_not_valid(query):
            return False
        return query

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if query_not_valid(query):
            message = b'{"message": "bad request, params could be only (id, name, tag, size,\
                                                            mimeType, modificationTime)"}'
            return self.write_response(404, message)
        path = urlparse(self.path).path
        if path_not_valid(path):
            return self.write_response(404, b'{"message": " Not Found"}')
        result = db.parse_from_db(query)
        if len(result) == 0:
            message = b'{"message": "No result"}'
            return self.write_response(204, message)
        # пока подразумеваем загрузку по 1 файлу
        if path == '/api/download':
            if len(query) > 1 or 'id' not in query.keys():
                message = b'{"message": "bad request, params could be only one id"}'
                return self.write_response(404, message)
            result = result[0]
            if len(result) == 0:
                return self.write_response(404, b'{"message": "404 Not Found"}')
            filename = get_name_from_file_id(result['id'])
            base_name = os.path.basename(filename)
            try:
                with open(filename, 'rb') as f:
                    body = f.read()
                file = bytes(body)
            except:
                pass
            self.send_response(200, "OK")
            self.send_header("Content-Type", result['mimeType'])
            self.send_header("Content-Disposition", 'filename={0}'.format(base_name))
            self.end_headers()
            return self.wfile.write(file)

        result_json = json.dumps(result).encode()
        return self.write_response(200, result_json)

    def do_POST(self):
        path = urlparse(self.path).path
        if path_not_valid(path):
            return self.write_response(404, b'{"message": "404 Not Found"}')
        size = int(self.headers['content-length'])
        modification_time = str(datetime.now().strftime('%Y:%m:%d_%H:%M:%S'))
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
        params = cgi.parse_multipart(self.rfile, pdict)
        content_type = params.get('content-type')[0] if 'content-type' in params else ctype
        file = params.get('file')[0]
        file_id = int(params.get('id')[0]) if 'id' in params else db.return_next_id()
        execution = os.path.splitext(self.headers.get_filename())[-1] if self.headers.get_filename() else ""
        name = params.get('name')[0] if 'name' in params else str(file_id)
        tag = params.get('tag')[0] if 'tag' in params else None
        # загрузка в ДБ
        data = {'id': int(file_id), 'name': name, 'tag': tag, 'size': size, 'mimeType': content_type,
                'modificationTime': modification_time}
        result = json.dumps(db.add_to_db(data))

        # upload in dir
        with open(UPLOADED_FILES_PATH + str(file_id) + execution, 'wb') as f:
            f.write(file)
            response = f"File '{name}'upload successfully!"
            print(response)
        return self.write_response(201, result)

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path_not_valid(path):
            return self.write_response(404, b'{"message": "404 Not Found"}')
        query = self.parse_query()
        if not query or len(query) == 0:
            message = b'{"message": "bad request, params could be only (id, name, tag, size,\
                                                                    mimeType, modificationTime)"}'
            return self.write_response(400, message)
        result = db.delete_from_db(query)
        if not result:
            return self.write_response(400, b'{"message": "No result"}')
        amount_del_files = delete_from_dir(result)
        message = {"message": "{0} files deleted".format(amount_del_files)}
        message_json = json.dumps(message)
        return self.write_response(200, message_json)


def runserver():
    try:
        print(f'http server is starting at address http://{URL}:{PORT}')
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
