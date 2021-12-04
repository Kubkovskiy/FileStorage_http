"""methods for FileStorage"""
import os


def create_dir(path="uploaded_files") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'

