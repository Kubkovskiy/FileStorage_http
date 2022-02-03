from requests import Response
import json

BASE_KEYS = ['id', 'name', 'tag', 'size', 'mimeType', 'modificationTime']


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Response is no JSON format, response text is {response.text}")
        assert name in expected_dict, f"Response JSON doesn't have key {name}"
        assert expected_dict[name] == expected_value, error_message

    @staticmethod
    def assert_expected_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code. Expected: {expected_status_code}, Actual: {response.status_code}"

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Response is no JSON format, response text is {response.text}")
        assert name in expected_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Response is no JSON format, response text is {response.text}")
        for name in names:
            assert name in expected_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Response is no JSON format, response text is {response.text}")
        for name in names:
            assert name not in expected_dict, f"Response JSON have key {name}"

    @staticmethod
    def base_assertions_for_positive_post_method(response: Response):
        """Check status code = 201,
        response is JSON and has ['id', 'name', 'tag', 'size', 'mimeType', 'modificationTime']"""
        Assertions.assert_expected_status_code(response, 201)
        Assertions.assert_json_has_keys(response, BASE_KEYS)

    @staticmethod
    def base_assertions_for_positive_get_method(response: Response):
        """Check status code = 200,
        response is JSON and all files has ['id', 'name', 'tag', 'size', 'mimeType', 'modificationTime']"""
        Assertions.assert_expected_status_code(response, 200)
        try:
            expected_dict = response.json()
            expected_name = BASE_KEYS
            for file in expected_dict:
                for name in expected_name:
                    assert name in file, f"Response JSON doesn't have key {name} in file: {file}"
        except json.JSONDecodeError:
            raise Exception(f"Response is no JSON format, response text is {response.text}")
