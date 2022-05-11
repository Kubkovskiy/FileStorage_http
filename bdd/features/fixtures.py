from behave import fixture
from lib.base_case import BaseCase


@fixture
def preparing_files_for_upload_and_delete_after_session(contex):
    contex.files = BaseCase.get_files()
    if len(contex.files) == 0:
        raise Exception('There are no files in upload_folders')
    yield contex.files
    # delete tests/files_for_upload/
    BaseCase.delete_upload_files(BaseCase.FILES_FOR_UPLOAD)