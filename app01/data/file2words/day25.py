#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
导入模块区
"""
import os
import random
import hashlib
from functools import reduce
import time
from collections import namedtuple
import sys

"""
求文件夹大小
"""


# import os
class ViewSize(object):

    def __init__(self):
        pass

    @staticmethod
    def view_file_size(path):
        size = os.stat(path).st_size
        return size

    @staticmethod
    def view_folder_size(path):

        file_size = 0
        folder_size = 0
        for folder_path_list, folder_list, file_list in os.walk(path):
            for file_name in file_list:
                file_size += os.stat(os.path.join(folder_path_list, file_name)).st_size
            for folder_name in folder_list:
                folder_size += os.stat(os.path.join(folder_path_list, folder_name)).st_size
                print(os.path.join(folder_path_list, folder_name), folder_size)
        return file_size, folder_size


####################################################
"""
验证文件一致性
"""


import os
from hashlib import md5


def confirm(path):
    confirm_obj = hashlib.md5()
    size = os.stat(path).st_size
    with open(path, 'rb') as f:
        while size > 1024:
            content = f.read(1024)
            confirm_obj.update(content)
            size -= 1024

        else:
            content = f.read(size)
            confirm_obj.update(content)
            size = 0
    return confirm_obj.hexdigest()


#
# print(confirm(r'D:\迅雷云盘\rebd-636.mp4'))

############################################
"""
抢红包，例：200RMB 10人
"""


# 200RMB 10人

# import random

def red_packet(money, people):
    res = random.sample(range(1, money * 100), people - 1)
    res.sort()
    res.insert(0, 0)
    res.append(money * 100)
    for i in range(len(res) - 1):
        yield (res[i + 1] - res[i]) / 100
    yield 'end'


#
#
# v1 = red_packet(200, 10)
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())
# print(v1.__next__())

#################################################
"""
super()：找多继承中的下一个类（mro算法）
"""


class A:

    def func(self):
        print('A')


class B(A):

    def func(self):
        print('B')
        super().func()
#
#
# v1 = B()
# v1.upload_file()
#####################################################
