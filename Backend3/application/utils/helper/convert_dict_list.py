

def convert_dict_list(target: dict) -> list:
    return [(k, v) for k, v in target.items()]


def convert_list_dict(target: list) -> dict:
    return {(k) for k in target}
