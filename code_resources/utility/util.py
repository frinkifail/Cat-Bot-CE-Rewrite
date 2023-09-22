from json import loads
from os import mkdir, path


def create_file(filename: str, default_data: str = ""):
    with open(filename, "w+") as f:
        f.write(default_data)
        f.close()


def init_data():
    def _():
        if not path.exists("data/timings.json"):
            create_file("data/timings.json", "{}")

    if not path.exists("data"):
        mkdir("data")
        _()
    elif path.exists("data"):
        _()


def read_file(filename: str):
    with open(filename, "r") as f:
        data = f.read()
    return data


def load_json(filename: str):
    return loads(read_file(filename))
