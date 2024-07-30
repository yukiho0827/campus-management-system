import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from app01 import models
from app01.utils.forms import TaskModelForm
from app01.utils.pagination import Pagination
from app01.utils import create_time
from app01.utils import random_str


def task_manage(request,code):
    # 分页搜索
    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        # 跨表查询
        data_list['user__user__contains'] = search_data
    # 解包查询条件 若为空会展示所有数据
    queryset = models.Task.objects.filter(**data_list).order_by("-level")

    form = TaskModelForm()
    page_obj = Pagination(request, queryset)

    # 时间
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = {
        'search_data': search_data,
        "form": form,
        'user_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),
        'time': time,
        'room_num': 1
    }
    return render(request, 'task_manage.html', content)


@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True,'code': random_str.create_random_str(5)}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def task_delete(request, uid):
    row_object = models.Task.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知数据'})
    row_object.delete()
    code = random_str.create_random_str(5)
    return redirect(f'/task/manage/{code}')


@csrf_exempt
def task_watch(request, uid):
    task = models.Task.objects.filter(id=uid).first()
    data_dict = {'cont1': task.title, 'cont2': task.detail}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
