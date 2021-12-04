# FileStorage main file
from http.server import HTTPServer, BaseHTTPRequestHandler
from FileStorage.methods import create_dir
import re

PORT = 9000
URL = '127.0.0.1'
UPLOADED_FILES_PATH = create_dir('uploaded_files')


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
        self.write_response(200)
        info = self.deal_post_data()
        self.wfile.write(f"200\n{info}".encode())
        print(info, "by: ", self.client_address)

    def remains_minus_line(self, remains_of_bytes: int):
        """read the next line and subtract lines length from the remainder"""
        line = self.rfile.readline()
        remains = remains_of_bytes - len(line)
        return (remains, line)

    def deal_post_data(self):
        uploaded_files = []
        boundary = self.headers.get_boundary().encode()
        if not boundary:
            return "Content-Type header doesn't contain boundary"
        remains_of_bytes = int(self.headers['content-length'])
        remains_of_bytes, line = self.remains_minus_line(remains_of_bytes)
        if boundary not in line:
            return "Content NOT begin with boundary"
        while remains_of_bytes > 0:
            remains_of_bytes, line = self.remains_minus_line(remains_of_bytes)
            fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())[0]
            if not fn:
                return "Can't find filename..."
            while len(line) > 2:
                remains_of_bytes, line = self.remains_minus_line(remains_of_bytes)
            try:
                out = open(UPLOADED_FILES_PATH + fn, 'wb')
            except IOError:
                return "Can't create file to write!!"
            else:
                with out:
                    pre_line = self.rfile.readline()
                    remains_of_bytes -= len(pre_line)
                    while remains_of_bytes > 0:
                        line = self.rfile.readline()
                        remains_of_bytes -= len(line)
                        if boundary in line:
                            pre_line = pre_line[0:-1]
                            if pre_line.endswith(b'\r'):
                                pre_line = pre_line[0:-1]
                            out.write(pre_line)
                            uploaded_files.append(fn)
                            break
                        else:
                            out.write(pre_line)
                            pre_line = line
        return "File '%s' upload success!" % ",".join(uploaded_files)


def run():
    print('server is start')
    server_address = (URL, PORT)
    server = HTTPServer(server_address, MyAwesomeHandler)
    server.serve_forever()


run()
