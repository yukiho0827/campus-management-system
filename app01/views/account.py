from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from datetime import datetime
from app01.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from app01.utils.forms import LoginForm
from app01.utils.code import check_code
from io import BytesIO


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 获取code必须放前面，Admin字段中没有code，不先删除code会报错
        input_code = form.cleaned_data.pop('code')

        admin_object1 = models.Admin.objects.filter(user=form.cleaned_data['user']).first()

        if not admin_object1:
            form.add_error('user', '用户名不存在。')

            return render(request, 'login.html', {'form': form})
        admin_object2 = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object2:
            form.add_error('password', '用户名或密码错误。')

            return render(request, 'login.html', {'form': form})

        # 超时获取可能为空
        code = request.session.get('image_code', '')
        if code.upper() != input_code.upper():
            form.add_error('code', '验证码错误。')

            return render(request, 'login.html', {'form': form})

        # 用户登录核心：
        request.session['info'] = {
            'id': admin_object2.id,
            'user': admin_object2.user,
        }
        # 3天免登录
        request.session.set_expiry(60 * 60 * 24 * 3)
        return redirect('/chart/manage/1')
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login')


def image_code(request):
    img, code_string = check_code()
    # 验证码写进session中
    request.session['image_code'] = code_string
    request.session.set_expiry(120)
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
