import json
import requests
from requests import Response


class BaseCase:
    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with the name {header_name} \
                                                in response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format, Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def upload_file_from_yandex_disk(self, url: str) -> bytes:
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = url  # Сюда вписываем ссылку на файл

        # Получаем загрузочную ссылку
        final_url = f"{base_url}public_key={url}"
        response = requests.get(final_url)
        download_url = response.json()['href']

        # Загружаем файл и возвращаем его
        download_response = requests.get(download_url)
        return download_response.content