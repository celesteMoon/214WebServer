from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy

from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="用户名", max_length=30)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "用户名或密码错误",
        "inactive": "该账号未激活, 请联系管理员 (你是怎么触发这条报错的???)",
    }


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, label='用户名')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='确认密码')

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("两次输入的密码不一致")