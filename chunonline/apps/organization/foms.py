# _*_ coding: utf-8 _*_
import re

__author__ = "andan"
__data__ = "2018/9/22 12:44"
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'moblie', 'course_name']

    def clean_moblie(self):
        moblie = self.cleaned_data['moblie']
        REGEX_MOBILE ="^1[3567890]\d{9}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(moblie):
            return moblie
        else:
            raise forms.ValidationError("手机号码非法",code="mobile_invaild")
