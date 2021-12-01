
from http.server import HTTPServer, BaseHTTPRequestHandler

from FileStorage.methods import get_filename

PORT = 9000
URL = '127.0.0.1'

class MyAwesomeHandler(BaseHTTPRequestHandler):
    def write_response(self,code: int):
        self.send_response(code)
        self.end_headers()


    def do_GET(self):
        self.write_response(200)
        headers = self.headers
        my_path = self.path
        self.wfile.write(my_path.encode())
        print(self.client_address)


    def do_POST(self):
        size = int(self.headers['Content-Length'])
        body = self.rfile.read(size)
        content_type = self.headers.get_content_type()
        boundary = self.headers.get_boundary()
        name = get_filename(boundary, body)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'This is POST request. ')
        self.wfile.write(b'Received: ')
        self.wfile.write(body)
        with open(f'file1', 'wb') as f:
            f.write(body)

"""
1)нужно сделать file_id через uuucn,
2) генерацию имени
3) модуль времени
4) прием параметров.

"""








def run():
    server_address = (URL, PORT)
    server = HTTPServer(server_address, MyAwesomeHandler)
    server.serve_forever()

run()