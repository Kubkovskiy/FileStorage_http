from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is no JSON format, response text is {response.text}"
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
            assert False, f"Response is no JSON format, response text is {response.text}"
        assert name in expected_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is no JSON format, response text is {response.text}"
        for name in names:
            assert name in expected_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            expected_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is no JSON format, response text is {response.text}"
        for name in names:
            assert name not in expected_dict, f"Response JSON have key {name}"
