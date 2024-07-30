from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from datetime import datetime
from app01.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from app01.utils.forms import LoginForm, AdminEditModelForm, AdminResetModelForm, AdminModelForm
from app01.utils.code import check_code
from io import BytesIO
from app01.utils import debug
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from app01.utils import random_str


@csrf_exempt
def admin_add(request):
    form = AdminModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        data_dict = {'status': True, "code": random_str.create_random_str(5)}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {'status': False, 'error': form.errors}

    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def admin_manage(request, code):
    # 获取查询内容
    search_data = request.GET.get('data', '')

    data_list = {}
    if search_data:
        # 根据字段名不同来设置
        data_list['user__contains'] = search_data
    # 解包导入查询条件
    queryset = models.Admin.objects.filter(**data_list)
    form = AdminModelForm()
    page_obj = Pagination(request, queryset)
    # with open('logs.txt', "a") as f:
    #     f.write(f"\n {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    #     print("写入文件")
    content = {
        "form": form,
        'search_data': search_data,
        'user_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),
    }
    return render(request, 'admin_manage.html', content)


def admin_delete(request, uid):
    row_object = models.Admin.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知数据'})
    row_object.delete()
    code = random_str.create_random_str(5)
    return redirect(f'/admin/manage/{code}')


def admin_edit(request, uid):
    row_object = models.Admin.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知数据'})
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        code = random_str.create_random_str(5)
        return redirect(f'/admin/manage/{code}')
    return render(request, 'admin_edit.html', {'form': form})


def admin_reset(request, uid):
    row_object = models.Admin.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {
            'msg': '未知数据',
        })
    if request.method == "GET":
        title = '重置密码--{}'.format(row_object.user)
        form = AdminResetModelForm()
        return render(request, 'admin_reset.html', {'msg': title, 'form': form, })
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        code = random_str.create_random_str(5)
        return redirect(f'/admin/manage/{code}')
    return render(request, 'admin_edit.html', {'form': form})
