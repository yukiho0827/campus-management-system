from app01 import models
from django.core.validators import ValidationError
from .bootstrap_modelform import BootStrapModelForm, BootStrapForm
from django import forms
from app01.utils import encrypt


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = models.Admin
        fields = ['user', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_user(self):
        user = self.cleaned_data.get('user')
        res = models.Admin.objects.filter(user=user).exists()
        if res:
            raise ValidationError('重复的用户名')
        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_password = encrypt.md5(password)
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm = encrypt.md5(self.cleaned_data.get('confirm_password'))
        if not password:
            return
        if confirm != password:
            raise ValidationError('两次输入的密码不一致,请重新输入。')


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['user']

    def clean_name(self):
        user = self.cleaned_data.get('user')
        res = models.Admin.objects.filter(user - user).first()
        if res:
            raise ValidationError('重复的用户名。')

        return user


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(),
        # widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = encrypt.md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('新密码不能与原密码相同')
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = encrypt.md5(self.cleaned_data.get('confirm_password'))
        if not pwd:
            return
        if confirm != pwd:
            raise ValidationError('两次输入的密码不一致,请重新输入。')
        # return confirm  # return的值会保存到数据库
        # （数据库中有对应字段的情况下）钩子方法会有很多操作空间


class LoginForm(BootStrapForm, forms.Form):
    user = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = encrypt.md5(pwd)
        return md5_pwd


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class QrcodeForm(BootStrapForm, forms.Form):
    name = forms.CharField(
        label='姓名',
        widget=forms.TextInput,
        required=True,
    )
    stu_number = forms.CharField(
        label='学号',
        widget=forms.TextInput,
        required=True,
    )
    phone_num = forms.CharField(
        label='手机号',
        widget=forms.TextInput,
        required=True,
    )
    temp = forms.CharField(
        label='体温',
        widget=forms.TextInput,
        required=True,
    )
    create_time = forms.DateTimeField(
        label='时间',
        widget=forms.DateTimeInput,
        required=True,
    )


class CleanForm(object):
    def clean_stu_number(self):
        stu_number = self.cleaned_data.get('stu_number')
        if len(stu_number) != 12:
            raise ValidationError('请输入正确格式的学号')
        return stu_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 11:
            raise ValidationError('请输入合法的手机号')
        return phone_number

    def clean_temp(self):
        temp = self.cleaned_data.get('temp')
        if 35 < float(temp) < 40:
            return temp
        raise ValidationError('请输入正确的体温')


class FormLibrary(CleanForm, BootStrapModelForm, forms.Form):
    class Meta:
        model = models.PlaceLibrary
        fields = "__all__"


class FormBasketballGround(CleanForm, BootStrapModelForm, forms.Form):
    class Meta:
        model = models.PlaceBasketballGround
        fields = "__all__"


class FormDiningRoom(CleanForm, BootStrapModelForm, forms.Form):
    class Meta:
        model = models.PlaceDiningRoom
        fields = "__all__"


class FormPlayground(CleanForm, BootStrapModelForm, forms.Form):
    class Meta:
        model = models.PlacePlayground
        fields = "__all__"
