from typing import Dict, Union


def parse_sentence(sentence: str) -> Dict:
    dict_ = {}
    parts = [part.strip() for part in sentence.split(' ')]

    for part in parts:
        kv = part.split('=')
        if len(kv) == 2:
            dict_[kv[0]] = parse_string(kv[1])

    return dict_


def parse_string(str_: str) -> Union[int, float, bool, str]:
    str_ = str_.strip()

    if str_.isnumeric():
        return int(str_)

    try:
        return float(str_)
    except ValueError:
        pass

    if str_.lower() in ['true', 'false']:
        return True if str_.lower() == 'true' else False

    return str_



