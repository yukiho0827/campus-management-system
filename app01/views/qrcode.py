from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import re
import os
import datetime
from app01 import models
from app01.utils import forms
# from app01.utils.form import TaskModelForm, QrcodeForm, FormLibrary, FormPlayground, FormDiningRoom, \
#     FormBasketballGround
from app01.utils.pagination import Pagination
from app01.utils.config import num2place, num2form, status_code, num2place_cn
from app01.utils import words_api, random_str, res2file
from app01.utils.decorators import *


@check_qrcode_time
def qrcode_form(request, place, res):
    if res:
        return render(request,'qrcode_pass.html')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == "GET":
        form_content = None
        if request.session:
            form_content = request.session.get('form_cont')
        if place in num2place:
            form = getattr(forms, num2form[place])(data=form_content)
        else:
            return render(request, 'error.html', {'msg': '未知页面'})

        return render(request, 'qrcode_form.html', {"form": form, "time": time, "place": num2place_cn[place]})

    if place in num2place:
        form = getattr(forms, num2form[place])(data=request.POST)
    else:
        return render(request, 'error.html')

    name = request.POST.get('name')
    stu_number = request.POST.get('stu_number')
    phone_number = request.POST.get('phone_number')
    temp = request.POST.get('temp')
    request.session["form_cont"] = {
        "name": name,
        "stu_number": stu_number,
        "phone_number": phone_number,
        "temp": temp,
        "place": num2place_cn[place],
    }
    request.session.set_expiry(60 * 60 * 24 * 30)

    if form.is_valid():
        form.save()
        request.session['create_info'] = True
        code = random_str.create_random_str(5)
        return redirect(f'/qrcode/file/result/{code}')

    return render(request, 'qrcode_form.html', {'form': form, "time": time})


def qrcode_upload_result(request, code):
    if request.method == "POST":
        # 获取图片对象
        result_code = request.FILES.get('data')
        # 拼接下载图片路径
        result_code_path = rf"{os.path.dirname(os.path.dirname(__file__))}\data\file2words\{result_code.name}"
        # 在拼接好的路径下下载图片
        with open(result_code_path, 'wb') as f:
            for chunk in result_code.chunks():
                f.write(chunk)
        ret = words_api.img2words(result_code_path, "result_code")
        if type(ret) == int:
            print("添加成功")
            request.session['result_code'] = ret
        else:
            print(type(ret))
        # return redirect('/qrcode/encrypt')
        code = random_str.create_random_str(5)
        return redirect(f'/qrcode/file/health/{code}')
    # print(request.session.get('place'))
    if not request.session.get('create_info'):
        return render(request, 'error.html', {'msg': '请返回上一步填写个人信息'})
    del request.session['create_info']
    return render(request, 'qrcode_upload_result.html', {"place": request.session.get('form_cont').get('place')})


def qrcode_upload_health(request, code):
    if request.method == 'POST':
        health_code = request.FILES.get('data')
        health_code_path = rf"{os.path.dirname(os.path.dirname(__file__))}\data\file2words\{health_code.name}"

        with open(health_code_path, 'wb') as f:
            for chunk in health_code.chunks():
                f.write(chunk)

        ret = words_api.img2words(health_code_path, "health_code")

        if type(ret) == int:
            request.session['health_code'] = ret
        code = random_str.create_random_str(5)
        return redirect(f'/qrcode/encrypt/{code}')

    if request.session.get('result_code') is None:
        return render(request, 'error.html', {'msg': '请返回上一步填写个人信息'})

    # del request.session['result_code']

    return render(request, 'qrcode_upload_health.html', {"place": request.session.get('form_cont').get('place')})


def qrcode_encrypt(request, code):
    if request.session.get('health_code'):
        total_code = request.session['result_code'] + request.session['health_code']
        print(f"核酸+健康码={total_code}")
        content = status_code[total_code]
        del request.session['health_code']
        print(f"状态码是{total_code}")
        res2file.write2file(total_code)
        if int(total_code) == 11:
            request.session['post_qrcode'] = '距上次提交不足三天'
            request.session.set_expiry(60 * 60 * 24 * 3)

        # 修改文件
        return render(request, "qrcode_encrypt.html",
                      dict(content, **{"place": request.session.get('form_cont').get('place')},
                           **{'res2wav': total_code}))

    return render(request, 'error.html', {'msg': '请先填写个人信息'})
