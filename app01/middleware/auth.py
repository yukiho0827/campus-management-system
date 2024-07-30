#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 后续还加  这里要改一下逻辑
        print(request.path_info)
        if request.path_info in ['/login', '/image/code', '/upload/manage', '/qrcode/1/form', '/qrcode/2/form',
                                 '/qrcode/3/form', '/qrcode/4/form', '/qrcode/encrypt', '/qrcode/form']:
            return
        # 正则表达式
        rule1 = re.compile(r"^/qrcode/file/result/\d+", re.S)
        rule2 = re.compile(r"^/qrcode/file/health/\d+", re.S)
        rule3 = re.compile(r"^/qrcode/encrypt/\d+", re.S)

        if rule1.findall(request.path_info) or rule2.findall(request.path_info) or rule3.findall(request.path_info):
            return

        print(request.path_info)

        info_dict = request.session.get('info')
        if not info_dict:
            return redirect('/login')
        return

    def process_response(self, request, response):
        return response
