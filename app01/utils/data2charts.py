from app01 import models


def show_data(month, days):
    # print(month, days)  # 6 [1, 2, 3, 4]
    days = days[::-1]
    exception = []
    total = []
    while days:
        day = days.pop()
        queryset_total = models.UploadImgInfo.objects.filter(create_time__month=month, create_time__day=day).count()
        total.append(queryset_total)
        queryset_health = models.UploadImgInfo.objects.filter(create_time__month=month, create_time__day=day,
                                                              res="体温正常").count()
        exception.append(queryset_total - queryset_health)
    return {"exception": exception,
            "total": total}
