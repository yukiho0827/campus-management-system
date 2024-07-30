#!/usr/bin/env python
# -*- coding:utf-8 -*-
import qrcode

data = r"http://47.104.203.134/qrcode/4/form"
filename = "篮球场.png"

img = qrcode.make(data)
img.save(filename)
