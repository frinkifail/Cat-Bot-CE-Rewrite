from json import loads


def read_file(filename: str):
    with open(filename, 'r') as f:
        return f.read()
def load_json(filename: str):
    return loads(read_file(filename))
