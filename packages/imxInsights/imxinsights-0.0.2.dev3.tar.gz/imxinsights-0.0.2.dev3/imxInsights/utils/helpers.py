import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from ruamel.yaml import YAML

# commented out: code that is not used but could be handy.


def get_yaml_dict(file_path):
    yaml = YAML()
    yaml.default_flow_style = True
    with open(file_path, "r") as stream:
        return yaml.load(stream)


# def save_dict_as_yaml(data, out_file_path):
#     yaml = YAML()
#     yaml.default_flow_style = True
#     with open(out_file_path, "w") as outfile:
#         yaml.dump(data, outfile)


def get_file_path(current_path: str, path: str) -> str:
    my_dir = os.path.dirname(current_path)
    config_file_path = os.path.join(my_dir, path)
    return config_file_path


# def is_float(element: Any) -> bool:
#     """
#     Check if a given value can be converted to a float.
#
#     :param element: The value to check.
#     :type element: any
#     :return: True if the value can be converted to a float, False otherwise.
#     :rtype: bool
#     """
#     if element is None:
#         return False
#     try:
#         float(element)
#         return True
#     except ValueError:
#         return False


def hash_dict_ignor_nested_values(dictionary: Dict):
    """Compute the hash of the dictionary's content."""
    new_dict = {}
    for key, value in dictionary.items():
        if not isinstance(value, dict):
            new_dict[key] = value

    hash_object = hashlib.sha1(json.dumps(new_dict, sort_keys=True).encode())
    return hash_object.hexdigest()


def flatten_dict(data_dict: Dict[str, Dict | str | List], skip_key: Optional[str] = "@puic", prefix="", sep=".") -> dict[str, str]:
    """
    Flattens a nested dictionary into a single level dictionary, where keys represent the full path to each leaf node.

    :param data_dict: The input dictionary to be flattened.
    :type data_dict: dict[str, dict | str | list]

    :param skip_key: The key to be skipped when processing nested dictionaries. Defaults to "@puic".
    :type skip_key: Optional[str]

    :param prefix: A prefix to be added to all flattened keys. Defaults to "".
    :type prefix: str

    :param sep: The separator to be used between key components. Defaults to ".".
    :type sep: str

    :return: A flattened dictionary where each key represents the full path to a leaf node, and each value is a string
    representation of the leaf node value.
    :rtype: dict[str, str]
    """
    result: Dict[str, str] = {}

    # Skip root node if this is a recursive call and key is found
    if prefix and skip_key in data_dict:
        return result

    for key, value in data_dict.items():
        if not isinstance(value, list) and not isinstance(value, dict):
            result[f"{prefix}{key}"] = value
            continue

        new_prefix = f"{prefix}{key}{sep}"

        if isinstance(value, list) and len(value) > 0 and not isinstance(value[0], dict):
            # ERMTS properties -> add index and add to current.
            for i, child in enumerate(value):
                result[f"{new_prefix}{i}"] = child
            continue

        # Multiple children -> list of dicts. Convert single dict to list with dict.
        if isinstance(value, dict):
            value = [value]

        assert len(value) > 0 and isinstance(value[0], dict)

        # Filter children with skip_key.
        remaining = list[dict]() if skip_key is not None else value
        if skip_key is not None:
            for child in value:
                if skip_key in child:
                    continue
                remaining.append(child)

        # Add index for each child if >1 and recurse, order can be changed in xml, so sort before indexing..
        if len(remaining) > 1:
            # sorting is done on a specified key.
            # if no key is present make hash of attributes, if no attributes hash first node attributes...
            # todo: add imx object sort keys to config yaml
            if key == "RailConnectionInfo":
                remaining = sorted(remaining, key=lambda x: x["@railConnectionRef"])
            elif key == "Announcement":
                remaining = sorted(remaining, key=lambda x: x["@installationRef"])
            else:
                remaining = sorted(remaining, key=hash_dict_ignor_nested_values)

        for i, child in enumerate(remaining):
            child_prefix = f"{new_prefix}{i}{sep}" if len(remaining) > 1 else new_prefix
            flattened = flatten_dict(child, skip_key=skip_key, prefix=child_prefix, sep=sep)
            result = result | flattened

    return result


def sha256sum(path: Path):
    return f"{hashlib.sha256(path.read_bytes()).hexdigest()}"
