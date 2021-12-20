"""methods for FileStorage"""
import os
import json
from copy import deepcopy

def create_dir(path="uploaded_files") -> str:
    """check is dir created."""
    if path in os.listdir():
        return path + '/'
    os.mkdir(path)
    return path + '/'


def list_to_json(result: list):
    copy_result = deepcopy(result)
    res = [[]]
    for i in copy_result:
        res[0].append(json.dumps(i))
    return res[0]