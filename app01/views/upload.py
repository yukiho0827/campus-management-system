from django.shortcuts import render, HttpResponse, redirect
from app01.utils import updatedb
import json
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from campus_management import settings
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from app01.utils.forms import LoginForm
from app01.utils.code import check_code
from app01.utils.config import num2place
from app01.utils import create_time


@csrf_exempt
def upload_manage(request):
    if request.method == "GET":
        return render(request, 'upload_manage.html')
    file_obj = request.FILES.get('data')
    zip_path = rf"{settings.zip_path}\{file_obj}"
    with open(zip_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    return redirect('/upload/manage')


def upload_show(request):
    if request.method == 'GET':
        queryset = models.UploadImgInfo.objects.all().order_by('-create_time')
        page_obj = Pagination(request, queryset)

        content = {
            'user_list': page_obj.page_queryset,
            'page_list_string': page_obj.show_page(),
        }

        return render(request, 'upload_show.html', content)
