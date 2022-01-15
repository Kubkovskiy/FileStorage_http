import requests


class MyRequests:
    @staticmethod
    def post(uri: str, data: dict = None, headers: dict = None, file: dict = None):
        return MyRequests._send(uri, data, headers, file, "POST")

        @staticmethod
        def get(uri: str, params: dict = None, headers: dict = None):
            return MyRequests._send(uri, params, headers, "GET")

        @staticmethod
        def put(uri: str, data: dict = None, headers: dict = None):
            return MyRequests._send(uri, data, headers, "PUT")

        @staticmethod
        def delete(uri: str, data: dict = None, headers: dict = None):
            return MyRequests._send(uri, data, headers, "DELETE")

    @staticmethod
    def _send(uri: str, data: dict, headers: dict, file: dict, method: str):

        url = f"http://127.0.0.1:9000/api/{uri}"
        if headers is None:
            headers = {}

        if method == "GET":
            response = requests.get(url, params=data, headers=headers)

        elif method == "POST":
            response = requests.post(url, data=data, headers=headers,files=file)

        elif method == "PUT":
            response = requests.put(url, data=data, headers=headers)

        elif method == "DELETE":
            response = requests.delete(url, data=data, headers=headers)

        else:
            raise Exception(f"Bad http method '{method}' was received")
        return response
