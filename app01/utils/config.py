#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime

time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
num2place_cn = {
    1: "图书馆",
    2: "操场",
    3: "餐厅",
    4: "篮球场",
}
num2place = {
    1: "PlaceLibrary",
    2: "PlacePlayground",
    3: "PlaceDiningRoom",
    4: "PlaceBasketballGround",
}
num2form = {
    1: "FormLibrary",
    2: "FormPlayground",
    3: "FormDiningRoom",
    4: "FormBasketballGround",
}

status_code = {
    4: {'res': False,
        'color': "danger",
        "content": '核酸证明核验失败，请检查：1.图片是否为核酸检测证明 2.是否在有效期内'},
    9: {'res': False,
        'color': "danger",
        "content": '核酸证明核验失败，请检查：1.图片是否为核酸检测证明 2.是否在有效期内'},
    11: {'res': True,
         'color': "success",
         "content": f'提交成功！当前时间：{time}'},
    5: {'res': False,
        'color': "danger",
        "content": '您的核酸检测结果为阳性，请立即隔离'},
    10: {'res': False,
         'color': "danger",
         "content": '您的核酸检测结果为阳性，请立即隔离'},
    6: {
        'res': False,
        'color': "danger",
        "content": '健康码核验失败，请重试',
    }
}
