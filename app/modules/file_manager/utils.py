import json
import os


def overwrite_file(path_to_file: str):
    if os.path.exists(path_to_file):
        os.remove(path_to_file)


def dict_to_json_file(dict: dict, path_to_file: str):
    with open(path_to_file, 'w') as f:
        json.dump(dict, f)