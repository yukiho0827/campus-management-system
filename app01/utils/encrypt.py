"""
md5加密
"""

import hashlib
# 调用django自带的盐
from django.conf import settings


def md5(data):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data.encode('utf-8'))
    return obj.hexdigest()
