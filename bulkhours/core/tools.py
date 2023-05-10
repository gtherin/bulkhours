import os
import json


def get_config():
    jsonfile = os.path.dirname(__file__) + "/../../.safe"
    if os.path.exists(jsonfile):
        with open(jsonfile) as json_file:
            return json.load(json_file)

    return {}


def get_value(key):
    return get_config().get(key)
