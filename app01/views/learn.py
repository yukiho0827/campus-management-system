import json

from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from datetime import datetime
from app01.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from app01.utils.forms import LoginForm
from app01.utils.code import check_code
from io import BytesIO
from app01.utils import unzip_obj


def learn_ajax(request):
    if request.method == 'POST':
        res1 = request.POST.get('data1')
        res2 = request.POST.get('data2')
        total = float(res1)+float(res2)
        v1 = unzip_obj.Unzip(request.POST)
        print(v1.unzip_req_post())
        print(request.POST)
        content = {'status': True, 'total': total}
        return HttpResponse(json.dumps(content))
    return render(request, 'learn_ajax.html')


def learn_api(request):
    if request.method == 'POST':
        data = {
            'status': True,
            'res': 102,
            'name': request.POST.get('name') or None,
        }
        return HttpResponse(json.dumps(data))
    return render(request, 'error.html', {'msg': None})
