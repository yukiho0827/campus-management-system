from django.shortcuts import render
from app01.utils import create_time, data2charts
from app01 import models


def chart_manage(request, info):
    # 实例化时间类的对象
    time_obj = create_time.CreateTime(models='l')
    # 获取时间字段
    time_fields = time_obj.get_time_field()
    # 取值
    month = time_fields['month']

    day = time_fields['day']
    # 判断开头是否为0
    if day.startswith('0'):
        day = day[1:]
    if month.startswith('0'):
        month = month[1:]

    days = [day for day in range(int(day) - 6, int(day) + 1) if day > 0]
    # 在获取数据的方法中传入时间 获取扫码异常人数与总人数
    charts_data = data2charts.show_data(month, days)
    exception = charts_data.get('exception')
    total = charts_data.get('total')

    # ###########################################
    # 给表2传递参数
    hour = time_fields['hour']
    if hour.startswith('0'):
        hour = hour[1:]
    hours = [hour for hour in range(int(hour) - 11, int(hour) + 1) if hour > 0]
    hours_filter = hours[::-1]
    temp = []
    humidity = []
    while hours_filter:
        hour_filter = hours_filter.pop()
        queryset = models.UploadFileData.objects.filter(create_time__day=day, create_time__month=month,
                                                        create_time__hour=hour_filter).values().first()

        if queryset:
            if queryset.get("temp"):
                temp.append(float(queryset.get("temp")))
                humidity.append(float(queryset.get("humidity")))
        else:
            temp.append(0)
            humidity.append(0)
    print(temp, humidity)
    # ############################################
    content = {
        "month": month,
        'days': days,
        'day': day,
        'hours': hours,
        'exception': exception,
        'total': total,
        "temp": temp,
        "humidity": humidity,
    }

    return render(request, f'chart_manage{info}.html', content)
