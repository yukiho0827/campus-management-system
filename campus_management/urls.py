"""campus_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import index, account, admin, task, chart, upload, photo, qrcode, placecode,learn

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', upload.upload_show),
    path('index', index.welcome),

    path('learn/ajax',learn.learn_ajax),
    path('login', account.login),
    path('logout', account.logout),
    path('image/code', account.image_code),

    path('admin/add', admin.admin_add),
    path('admin/manage/<int:code>', admin.admin_manage),
    path('admin/<int:uid>/delete', admin.admin_delete),
    path('admin/<int:uid>/edit', admin.admin_edit),
    path('admin/<int:uid>/reset', admin.admin_reset),

    path('task/manage/<int:code>', task.task_manage),
    path('task/add', task.task_add),
    path('task/<int:uid>/delete', task.task_delete),
    path('task/<int:uid>/watch', task.task_watch),

    path('chart/manage/<int:info>', chart.chart_manage),

    path('upload/manage', upload.upload_manage),
    path('upload/show', upload.upload_show),


    path('photo/view', photo.photo_view),

    path('placecode/<int:place>/manage', placecode.place_code_manage),

    path('qrcode/<int:place>/form', qrcode.qrcode_form),
    path('qrcode/file/result/<int:code>', qrcode.qrcode_upload_result),
    path('qrcode/file/health/<int:code>', qrcode.qrcode_upload_health),
    path('qrcode/encrypt/<int:code>', qrcode.qrcode_encrypt),



]
