#_*_ coding: utf-8 _*_ 
__author__ = "andan"
__data__ = "2018/9/28 17:33"

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/user/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)