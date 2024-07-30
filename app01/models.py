import django.utils.timezone
from django.db import models


class Admin(models.Model):
    user = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.user


class AbnormalInfo(models.Model):
    num = models.BigIntegerField(verbose_name='学号')
    photo_path = models.CharField(verbose_name='路径', max_length=64)
    temperature = models.FloatField(verbose_name='体温')


class Task(models.Model):
    level_choices = (
        (3, '紧急'),
        (2, '重要'),
        (1, '临时'),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    create_time = models.DateField(verbose_name='发起时间')
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)
    detail = models.TextField(verbose_name="正文")


class PlaceLibrary(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    stu_number = models.CharField(verbose_name="学号", max_length=32)
    phone_number = models.CharField(verbose_name="手机号", max_length=32)
    create_time = models.DateTimeField(verbose_name='时间')
    temp = models.CharField(verbose_name="体温", max_length=32)


class PlacePlayground(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    stu_number = models.CharField(verbose_name="学号", max_length=32)
    phone_number = models.CharField(verbose_name="手机号", max_length=32)
    create_time = models.DateTimeField(verbose_name='时间')
    temp = models.CharField(verbose_name="体温", max_length=32)


class PlaceBasketballGround(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    stu_number = models.CharField(verbose_name="学号", max_length=32)
    phone_number = models.CharField(verbose_name="手机号", max_length=32)
    create_time = models.DateTimeField(verbose_name='时间')
    temp = models.CharField(verbose_name="体温", max_length=32)


class PlaceDiningRoom(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    stu_number = models.CharField(verbose_name="学号", max_length=32)
    phone_number = models.CharField(verbose_name="手机号", max_length=32)
    create_time = models.DateTimeField(verbose_name='时间')
    temp = models.CharField(verbose_name="体温", max_length=32)


class UploadFileData(models.Model):
    temp = models.CharField(verbose_name="温度", max_length=16)
    humidity = models.CharField(verbose_name="相对湿度（单位：%）", max_length=16)
    co2 = models.CharField(verbose_name="二氧化碳浓度", max_length=16)
    liquid = models.CharField(verbose_name="液体澄清程度", max_length=16)
    gas = models.CharField(verbose_name="气体压力程度", max_length=16)
    create_time = models.DateTimeField(verbose_name="时间")


class UploadImgInfo(models.Model):
    create_time = models.DateTimeField(verbose_name="时间")
    res = models.CharField(verbose_name="体温情况", max_length=16)
    photo = models.CharField(verbose_name="人像", max_length=128)
