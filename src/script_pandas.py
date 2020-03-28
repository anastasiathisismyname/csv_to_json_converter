import pandas as pd
import os.path
import os
import json

root_dir = "\\".join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1])


def get_json_data(path):
    df = pd.read_csv(path)
    filename = path.split('\\')[-1]
    df.to_json(f"{root_dir}\\returned_json_files\\{filename}")
    with open(f"{root_dir}\\returned_json_files\\{filename}") as f:
        return json.loads(f.read())


def delete_file(path):
    os.remove(path)