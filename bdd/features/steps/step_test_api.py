from behave import given, then
from bdd.main import print_tests

FILES_FOR_UPLOAD = ""
BASE_SERVER_URL = ""
URL_TO_ARCHIVE = ""
BASE_KEYS = []
FILES_LIST = []


@given("Set base server url is {server_url}")
def step_impl(contex, server_url):
    global BASE_SERVER_URL
    BASE_SERVER_URL = server_url


@given("Set the path to default folder for upload files to server is {files_for_upload}")
def step_impl(contex, files_for_upload):
    global FILES_FOR_UPLOAD
    FILES_FOR_UPLOAD = files_for_upload


@given("Set the responses base keys is {base_keys}")
def step_impl(contex, base_keys):
    global BASE_KEYS
    BASE_KEYS = base_keys


@given("for tests a = {a}")
def setp_impl(contex, a):
    contex.result = print_tests(a)


@then("should return {result}")
def step_impl(contex, result):
    assert int(contex.result) == result, f'что-то не так.. должно быть {result}, а по факту {contex.result}'