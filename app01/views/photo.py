#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import re
from app01 import models
from app01.utils.forms import TaskModelForm
from app01.utils.pagination import Pagination
import time
import os
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def photo_view(request):
    if request.method == "GET":
        return render(request, 'photo_view.html')
    file_obj = request.FILES.get('data')
    zip_path = rf"{os.path.dirname(os.path.dirname(__file__))}\data\zip\{file_obj.name}"
    f = open(zip_path, 'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    # updatedb.unzip(updatedb.zip_folder_path, rf'{updatedb.save_folder_path}\img', rf'{updatedb.save_folder_path}\info')
    # updatedb.update_db(rf'{updatedb.save_folder_path}\info')
    time.sleep(3)
    return redirect('/photo/view')
