from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.config import num2place
from app01.utils import create_time


def place_code_manage(request, place):

    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        # 根据字段名不同来设置
        data_list['name__contains'] = search_data
    # 反射找到对应属性
    if place in num2place:
        queryset = getattr(models, num2place[place]).objects.filter(**data_list).order_by('-create_time')
    else:
        queryset = models.PlaceLibrary.objects.filter(**data_list).order_by('-create_time')
    page_obj = Pagination(request, queryset)
    # 当日扫码人数动态展示
    time_obj = create_time.CreateTime()
    time_fields = time_obj.get_time_field()
    year, month, day = time_fields['year'], time_fields['month'], time_fields['day']
    people_num_list = []
    for place_name in num2place.values():
        filter_time_queryset = getattr(models, place_name).objects.filter(create_time__year=year,
                                                                          create_time__month=month,
                                                                          create_time__day=day)
        people_num_list.append(len([*filter_time_queryset]))
    content = {
        'search_data': search_data,
        'user_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),
        "num": place,
        'people_num_list': people_num_list,
    }
    return render(request, "place_code_manage.html", content)