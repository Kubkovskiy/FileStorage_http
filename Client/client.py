import requests

PORT = 9000
URL = 'http://127.0.0.1:{}'.format(PORT)


def get():
    r = requests.get(URL)
    print(r.text)

#
# def post(file):
#     """fot upload binary files"""
#     with open(file, 'rb') as f:
#         data = f.read()
#         params = {'name': file, 'tag`': 'txt', "file_id": None}
#         r = requests.post(URL, data=data, params=params)
#         print(r.text)


def post_multy(file):
    files = {'file': (file, open(file, 'rb'))}
    params = {'name': file, 'tag': 'txt', "file_id": None}
    r = requests.post(URL, files=files, params=params)
    print(r.status_code, r.text)


post_multy('1 Москва.xlsx')
# post('1 Москва.xlsx')
