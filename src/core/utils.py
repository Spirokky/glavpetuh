import re
import string


def clean_data(dct):
    cleaned = {}
    for k, v in dct.items():
        cleaned[k] = re.sub('\\n', '', v)
    return cleaned


def validate_nickname(nickname):
    for char in nickname:
        if char in string.punctuation + string.whitespace:
            return 1
    pattern = re.compile('[а-яА-ЯёЁ]')
    match = re.search(pattern, nickname)
    if match:
        return 2
    else:
        return 3


if __name__ == '__main__':
    pass
