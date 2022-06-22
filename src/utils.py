import json
import src.Coord

VERBOSE = False


def is_json(message):
    try:
        json.loads(message)
    except ValueError as e:
        return False
    return True


def centre_shape(x, y, w, h):
    c_x = (x + w) / 2
    c_y = (y + h) / 2
    return [c_x, c_y]
