from lib.base_case import BaseCase
import pytest

URL_TO_ARCHIVE = "https://disk.yandex.ru/d/aJoFOPqLRHGGXw"

@pytest.fixture(scope='session')
def preparing_files_for_upload():
    """download from public link and extract to tests/files_for_upload/ folder
    after tests folder should be deleted '"""
    print('\n === Start session ===')
    print(f'\n Download files from {URL_TO_ARCHIVE} ')
    print(f'\n Extract archive to {BaseCase.FILES_FOR_UPLOAD} ')
    files = BaseCase.download_and_extract_zip_archive_from_cloud(URL_TO_ARCHIVE)
    print(' \n === TESTING === \n')
    yield files
    import shutil
    # delete upload folder
    print("\n Deleting upload folder")
    shutil.rmtree(BaseCase.FILES_FOR_UPLOAD)
    print('\n === Finish session === \n')