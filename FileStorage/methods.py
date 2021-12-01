from http.server import HTTPServer, BaseHTTPRequestHandler

def get_filename(boundary, body):
    metadata = body.decode('latin-1').split(boundary)
    discription = metadata[1].split('\r\n')
    _, _, filename = discription[1].split(';')
    index = filename.find('"')
    name = filename[index+1:-1]
    return name
