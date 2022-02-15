import json
from behave import given, then, when
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

global_variables = {}
http_request_header = {}
http_request_file = {}
http_request_data = {"file_id": None, "name": None, "tag": None, "content_type": None}


# Background
@given('Set base server url as "{base_server_url}"')
def step_impl(contex, base_server_url):
    global_variables['base_server_url'] = base_server_url


@given('Set the path to default folder for upload files to server as "{upload_folder_path}"')
def step_impl(contex, upload_folder_path):
    global_variables['upload_folder_path'] = upload_folder_path


@given('Set the responses base keys as "{base_keys}"')
def step_impl(contex, base_keys):
    base_keys_list = base_keys.split(',')
    global_variables['base_keys'] = base_keys_list


@given(u'Set which files should be upload as "{file_names}"')
def step_impl(contex, file_names):
    file_names_list = file_names.split(',')
    global_variables['file_names'] = file_names_list


@given(u'Set link to zip_archive or files for test in the cloud as "{link_to_test_files}"')
def step_impl(contex, link_to_test_files):
    global_variables['url_to_archive'] = link_to_test_files


# end Background

@given(u'Set api endpoint as "{endpoint}"')
def step_impl(context, endpoint):
    endpoint = endpoint.lower()
    if endpoint == 'get':
        global_variables['endpoint'] = 'get'
    elif endpoint == 'upload':
        global_variables['endpoint'] = 'upload'
    elif endpoint == 'delete':
        global_variables['endpoint'] = 'delete'
    elif endpoint == 'download':
        global_variables['endpoint'] = 'download'
    else:
        raise Exception(f'Bad requests method! expected [GET, POST, DELETE, DOWNLOAD], actual: {endpoint}')


@when(u'Set HEADER param content type as "{content_type}"')
def step_impl(context, content_type):
    content_type = content_type.lower()
    http_request_data['content_type'] = content_type


@when(u'Set "{key}" as "{value}"')
def step_impl(context, key, value):
    if key == "file id":
        assert value.isdigit(), f"Wrong id. Should be digit, actual {value}"
        value = int(value)
        key = 'file_id'
    elif key in ["content_type", "content-type", "content type"]:
        key = 'content_type'
    http_request_data[key] = value


@when(u'Set file "{file_name}" as body')
def step_impl(context, file_name):
    file_dict = BaseCase.open_file_from_upload_folder(file_name)
    http_request_file.update(file_dict)


@then(u'Raise "{http_request_type}" HTTP request')
def step_impl(context, http_request_type):
    http_request_type = http_request_type.lower()
    endpoint = global_variables['endpoint']
    file_id = http_request_data['file_id']
    name = http_request_data['name']
    tag = http_request_data['tag']
    content_type = http_request_data['content_type']
    if http_request_type == 'post':
        file = http_request_file
        data, headers, payload = BaseCase.set_data_to_post_method(file, file_id, name, tag, content_type)
        context.response = MyRequests.post(endpoint, data, headers, payload)


@then("Response http code should be {status_code}")
def step_impl(context, status_code):
    expected_status_code = int(status_code)
    actual_status_code = context.response.status_code
    assert actual_status_code == expected_status_code, \
        f'Response http code should be {status_code}, actual: {actual_status_code}'


@then(u'Response content should have base keys "{base_keys}"')
def step_impl(context, base_keys):
    base_keys = base_keys.replace(' ', '')
    expected_base_keys = base_keys.split(',')
    response = context.response
    Assertions.assert_json_has_keys(response, expected_base_keys)


@then(u'Response content "{key}" should be "{value}"')
def step_impl(context, key, value):
    response_dict = context.response.json()
    actual = response_dict[key]
    if key == "id":
        assert value.isdigit(), f"Wrong id. Should be digit, actual {value}"
        expected_value = int(value)
    else:
        expected_value = value
    Assertions.assert_json_value_by_name(context.response, key, expected_value,
                                         f"Response '{key}' expected {value} , actual {actual}")


@then(u'Response content should be JSON format')
def step_impl(context):
    response = context.response
    try:
        response.json()
    except json.JSONDecodeError:
        raise Exception(f"Response is no JSON format, response text is {response.text}")
