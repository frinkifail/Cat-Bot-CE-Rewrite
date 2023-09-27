from json import dump, dumps, load, loads
from os import mkdir, path
from typing import Any, Literal

ValidDataFilenames = Literal[
    "data/timings.json",
    "data/cats.json",
    "dev/TOKEN.txt",
    "data/cattype.json",
    "data/cscwg.json",
]
ValidUpdateModes = Literal["replace", "add", "subtract"]

EMOJI_GUILD_ID = 1151848215071703103

# region File Manager Utilities


def create_file(filename: str, default_data: str = ""):
    with open(filename, "w+") as f:
        f.write(default_data)
        f.close()


def init_data():
    def _():
        if not path.exists("data/timings.json"):
            create_file("data/timings.json", "{}")
        if not path.exists("data/cats.json"):
            create_file("data/cats.json", "{}")
        if not path.exists("data/cattype.json"):
            create_file("data/cattype.json", "{}")
        if not path.exists("data/cscwg.json"):
            create_file("data/cscwg.json", "{}")
        if not path.exists("data/achs.json"):
            create_file("data/achs.json", "{}")

    if not path.exists("data"):
        mkdir("data")
        _()
    elif path.exists("data"):
        _()


def read_file(filename: ValidDataFilenames):
    with open(filename, "r") as f:
        data = f.read()
    return data


def write_file(filename: ValidDataFilenames, data: str):
    with open(filename, "w") as f:
        f.write(data)


def load_json(filename: ValidDataFilenames):
    return loads(read_file(filename))


def save_json(dictionary: dict[Any, Any], filename: ValidDataFilenames):
    data = dumps(dictionary)
    write_file(filename, data)


def update_json(
    new_dictionary: dict[Any, Any],
    filename: ValidDataFilenames | None = None,
    dictionary: dict | None = None,
    load_file: bool = False,
):
    if (dictionary is None and filename is not None) or (
        load_file and filename is not None
    ):
        current_data: dict[Any, Any] = load_json(filename)
    elif dictionary is not None and load_file is False:
        current_data = dictionary
    else:
        print("[ERROR] Invalid statement")
        return
    current_data.update(new_dictionary)
    if filename is not None:
        save_json(current_data, filename)
    else:
        print(
            "[WARNING] Could not save to json file: No path specified\n- Returning current data instead"
        )
        return current_data
    print(f"[SUCCESS] Successfully updated {filename}")


# endregion


# region New DB Stuff
class JsonLoadedDict(dict):
    def __getitem__(self, key: str | int) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError:
            try:
                with open(f"data/{key}.json", "r") as f:
                    item = load(f)
                self.__setitem__(key, item)
                return item
            except Exception as e:
                raise KeyError(f"This is a KeyError raised by JsonLoadedDict: {e}")

    def reload(self, key: str | int):
        try:
            with open(f"data/{key}.json", "r") as f:
                item = load(f)
            self.__setitem__(key, item)
        except Exception as e:
            raise UserWarning(
                f"This is a KeyError raised by JsonLoadedDict's reload method: {e}"
            )

    def save(self, key: str):
        with open(f"data/{key}.json", "w") as f:
            dump(self.get(key), f)


db = JsonLoadedDict()


# the most pain of shit but thanks anyway
# Try Except Value Create New Object In Object
def tevcnoio(value: Any | None, key: str | int, new_object: Any, in_object: dict):
    if value is None:
        in_object.__setitem__(key, new_object)
        return new_object
    else:
        return value


# endregion
