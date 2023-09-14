import json

def read(file_path, cred):
    with open(file_path, "r") as json_file:
        config_data = json.load(json_file)
    config = config_data.get(cred,{})
    return config