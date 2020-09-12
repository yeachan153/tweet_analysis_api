import json


def read_json(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)
