# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    #用passwordinput控件来渲染html input元素,属性为type="password"


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)  #注意只有这两项需要cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):  #在is_valid方法执行时会自动执行
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords don't match.")
        return cd['password2']