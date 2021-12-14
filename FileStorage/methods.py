"""methods for FileStorage"""
import os
import uuid
import datetime


def check_name_in_params(params: dict) -> bool:
    return True if 'name' in params else False




def generate_filename(file_id: str, filename = None):
    if filename:
        filename, execution = os.path.splitext(filename)
        return file_id, execution
    return file_id



def create_dir(path="uploaded_files") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'


