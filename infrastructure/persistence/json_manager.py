import json
import os

BASE_PATH = "data"

def ensure_data():
    os.makedirs(BASE_PATH, exist_ok=True)

def read_json(file):
    path = f"{BASE_PATH}/{file}"
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def write_json(file, data):
    path = f"{BASE_PATH}/{file}"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
