import json
import os
import numpy as np


def load_file_json(json_path: str) -> dict:
    """Loads json data from a file.
    Args:
        json_path: the path to the json file.
    Returns:
        json_data: a dict of the json data.
    """
    with open(json_path) as f:
        json_data = json.load(f)
        return json_data


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def write_file_json(json_path: str, json_dict: dict):
    """Writes json to file.
    This function will write over the original file if it exists.
    Args:
        json_path: the path to the json file.
        json_dict: the dict containing the json to write to file.
    """
    json_dir, _ = os.path.split(json_path)
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir, exist_ok=True)
    with open(json_path, "w") as outfile:
        print(f"Outfile: {outfile}")
        json.dump(json_dict, outfile, indent=2, cls=NpEncoder)