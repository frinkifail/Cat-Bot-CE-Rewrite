from json import dumps, loads
from os import mkdir, path
from typing import Any, Literal

ValidDataFilenames = Literal["data/timings.json", "data/cats.json", "dev/TOKEN.txt"]
ValidUpdateModes = Literal["replace", "add", "subtract"]


# |< Unused functions because I gave up on utility stuff
# region AI Generated Fun
# def get_recursive_dict(dictionary: dict[Any, Any], subkeys: list[str | int]):
#     """
#     Recursively gets the value of a nested dictionary using a list of subkeys.

#     Args:
#         dictionary: The nested dictionary.
#         subkeys: A list of subkeys.

#     Returns:
#         The value of the nested dictionary at the specified subkeys.
#     """

#     if len(subkeys) == 1:
#         return dictionary[subkeys[0]]
#     else:
#         return get_recursive_dict(dictionary[subkeys[0]], subkeys[1:])


# def set_recursive_dict(dictionary: dict[Any, Any], subkeys: list[str], value: Any):
#     """
#     Recursively sets the value of a nested dictionary using a list of subkeys.

#     Args:
#         dictionary: The nested dictionary.
#         subkeys: A list of subkeys.
#         value: The value to set.

#     Returns:
#         None.
#     """

#     if len(subkeys) == 1:
#         dictionary[subkeys[0]] = value
#     else:
#         if subkeys[0] not in dictionary:
#             dictionary[subkeys[0]] = {}

#         set_recursive_dict(dictionary[subkeys[0]], subkeys[1:], value)


# def update_recursive_dict(
#     dictionary: dict[Any, Any],
#     subkeys: list[str],
#     new_updated: dict[Any, Any],
#     mode: ValidUpdateModes = "replace",
#     amount: float | int = 0,
# ):
#     """
#     Recursively updates the value of a nested dictionary using a list of subkeys and a new updated dictionary.

#     Args:
#         dictionary: The nested dictionary.
#         subkeys: A list of subkeys.
#         new_updated: A new updated dictionary.

#     Returns:
#         None.
#     """
#     print(mode)
#     if len(subkeys) == 1:
#         if dictionary.get(subkeys[0]) is not None:
#             dictionary[subkeys[0]].update(new_updated)
#         else:
#             dictionary[subkeys[0]] = {}
#             dictionary[subkeys[0]].update(new_updated)
#             print("shiver me timbers")
#     else:
#         if subkeys[0] not in dictionary:
#             if mode != "add" or mode != "subtract":
#                 dictionary[subkeys[0]] = {}
#             else:
#                 dictionary[subkeys[0]] = 0
#         elif subkeys[0] in dictionary:
#             if mode == "add" and amount != 0:
#                 dictionary[subkeys[0]] += amount
#             elif mode == "subtract" and amount != 0:
#                 dictionary[subkeys[0]] -= amount

#         update_recursive_dict(dictionary[subkeys[0]], subkeys[1:], new_updated, mode)


# endregion


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


def try_get(dictionary: dict[Any, Any], key: str, default: Any = "<unset>"):
    data = dictionary.get(key)
    if data is None:
        dictionary[key] = default
    else:
        pass
    return dictionary


def update_json(
    new_dictionary: dict[Any, Any],
    filename: ValidDataFilenames | None = None,
    dictionary: dict | None = None,
):
    if dictionary is None and file:
        current_data: dict[Any, Any] = load_json(filename)
    else:
        current_data = dictionary
    current_data.update(new_dictionary)
    # if mode == "replace" and isinstance(dictionary, dict):
    #     if subkeys.__len__() == 0:
    #         current_data.update(dictionary)
    #     else:
    #         update_recursive_dict(current_data, subkeys, dictionary)
    # elif mode == "add" and (
    #     isinstance(dictionary, int) or isinstance(dictionary, float)
    # ):
    #     update_recursive_dict(current_data, subkeys, {}, "add", dictionary)
    save_json(current_data, filename)
    print(f"[SUCCESS] Successfully updated {filename}")
