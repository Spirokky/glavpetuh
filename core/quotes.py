import random
import time
import config


def quote():
    t = time.time()
    random.seed(t)
    lst = config.quotes
    arr_len = len(lst) - 1
    i = random.randint(0, arr_len)
    return lst[i]


if __name__ == '__main__':
    pass