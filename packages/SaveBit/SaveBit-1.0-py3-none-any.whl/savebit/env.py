format_data = {
    "pickle": {
        "type": ["str", "int", "float", "list", "tuple", "dict", "set", "bytes", "func"]
    },
    "json": {"type": ["str", "int", "list", "dict"]},
    "yaml": {"type": ["str", "int", "list", "dict"]},
    "ini": {"type": ["dict"]},
}


def get_data_type(data: object):
    if isinstance(data, int):
        return "int"
    elif isinstance(data, str):
        return "str"
    elif isinstance(data, list):
        return "list"
    elif isinstance(data, dict):
        return "dict"
    elif hasattr(data, "__call__"):
        return "func"
    elif hasattr(data, float):
        return "float"
    elif hasattr(data, set):
        return "set"
    elif hasattr(data, tuple):
        return "tuple"
    elif hasattr(data, bytes):
        return "byte"
    else:
        return "unknown"
