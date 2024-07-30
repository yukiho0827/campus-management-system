import random


def create_random_str(num):
    ret = []
    for _ in range(num):
        ret.append(str(random.randint(1, 9)))
    return "".join(ret)
