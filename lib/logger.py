import datetime
import os
from requests import Response


def create_dir(path="logs"):
    """check is dir created."""
    if path not in os.listdir():
        os.mkdir(path)
        return True
    return True


class Logger:
    modification_time = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    file_name = f"logs/log_{modification_time}.log"
    is_dir_created = create_dir('logs')

    @classmethod
    def _write_data_to_log(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as file_logger:
            file_logger.write(data)

    @classmethod
    def add_requests(cls, url: str, data: dict, headers: dict, method: str):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = "\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {cls.modification_time}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        cls._write_data_to_log(data_to_add)

    @classmethod
    def add_response(cls, response:Response):
        headers_dict = dict(response.headers)
        data_to_add = f"Response status_code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_dict}\n"
        cls._write_data_to_log(data_to_add)

    @classmethod
    def add_test_results(cls, data: str):
        data_to_add = f"Test result: {data}\n"
        cls._write_data_to_log(data_to_add)






