# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    #用passwordinput控件来渲染html input元素,属性为type="password"