import json


def is_json(message):
    try:
        json.loads(message)
    except ValueError as e:
        return False
    return True
