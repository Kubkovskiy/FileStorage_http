"""methods for FileStorage"""
import os

from FileStorage.main import UPLOADED_FILES_PATH


def create_dir(path="uploaded_files") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'

def get_name_from_file_id(file_id):
    for file in os.scandir(UPLOADED_FILES_PATH):
        name, execution = os.path.splitext(file.name)
        if name == str(file_id):
            return file.path


def delete_from_dir(result: [dict]) -> int:
    """take dict, deleting by file_id. return amount of deleted files"""
    count = len(result)
    for i in result:
        name_from_db = get_name_from_file_id(i['id'])
        os.remove(name_from_db)
        print(f"{name_from_db} was deleted successfully")
    return count


def path_not_valid(path):
    valid_api = ['/api/get', '/api/upload', '/api/delete', '/api/download']
    if path not in valid_api:
        return True


def query_not_valid(query: dict):
    valid_query = ['id', 'name', 'tag', 'size', 'mimeType', 'modificationTime', '']
    for param in query.keys():
        if param not in valid_query:
            return True