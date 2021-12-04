import requests

PORT = 9000
URL = 'http://127.0.0.1:{}'.format(PORT)


def get():
    r = requests.get(URL)
    print(r.text)


def post():
    p = requests.post(URL)
    print(p.text)


def post_form_data(file: str):
    files = {'file': (file, open(file, 'rb'))}
    r = requests.post(URL, files=files)
    print(r.text)
# post_form_data('12.doc')


def post_post(file):

    files = {'file': (file, open(file, 'rb'), "multipart/form-data")}
    r = requests.post(URL, files=files)
    print(r.text)

post_post('test.xlsx')