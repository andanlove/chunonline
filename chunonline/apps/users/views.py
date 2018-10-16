import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from utils.email_send import email_register_send
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForms, RegisterForms, ForgetForms, ModifyPwdForms, UploadImageForms, UserInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner


# 登录逻辑的重写
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 用户名和邮箱都可以作为账户
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 激活邮箱账号
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 取出邮箱发送的验证字符串的信息
        if all_records:
            for recorde in all_records:
                email = recorde.email
                user = UserProfile.objects.get(email=email)  # 匹配用户的邮箱
                user.is_active = True  # 激活
                user.save()
                return redirect('login')
                # return redirect()
        else:
            return render(request, 'active.html')


# 注册验证，发送邮件
class Register(View):
    def get(self, request):
        register_form = RegisterForms()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForms(request.POST)  # 表单验证
        if register_form.is_valid():  # 表单验证是否通过
            pass_word = request.POST.get("password")  # 获取用户信息
            user_name = request.POST.get("email")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {'msg': "用户已存在", 'register_form': register_form})

            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)  # 密码加密
            user_profile.save()
            email_register_send(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})


# 登录验证
class User_login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username")
            pass_word = request.POST.get("password")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("index")
                else:
                    return render(request, "login.html", {"msg": "请激活邮箱"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 修改密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForms()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForms(request.POST)
        email = request.POST.get("email")
        if forget_form.is_valid():
            email_register_send(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'email': email})

#
class ResetUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 取出邮箱发送的验证字符串的信息
        if all_records:
            for recorde in all_records:
                email = recorde.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'forgetpwd.html')

#找回密码
class ModifyView(View):
    def post(self, request):
        modify_form = ModifyPwdForms(request.POST)
        if modify_form.is_valid():
            pw1 = request.POST.get("password1")
            pw2 = request.POST.get("password2")
            email = request.POST.get("email")
            if pw1 != pw2:
                return render(request, 'forgetpwd.html', {'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pw2)
            user.save()
            return render(request, 'index.html')
        else:
            return render(request, 'forgetpwd.html', {'modify_form': modify_form})

#用户信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'usercenter-info.html', {'user': user})

    def post(self, request):
        user_info = UserInfoForm(request.POST, instance=request.user)
        if user_info.is_valid():
            user_info.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dump(user_info.errors), content_type='application/json')


class UploadImageView(View):
    def post(self, request):
        imge_forms = UploadImageForms(request.POST, request.FILES, instance=request.user)
        if imge_forms.is_valid():
            imge_forms.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

#更改密码
class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForms(request.POST)
        if modify_form.is_valid():
            pw1 = request.POST.get("password1")
            pw2 = request.POST.get("password2")
            if pw1 != pw2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pw2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

#发送验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"msg":"邮箱已注册"}', content_type='application/json')
        email_register_send(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''
    修改个人邮箱
    '''

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        exist_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if exist_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class MyFavOrg(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavCourse(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyFavTeacher(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })

#用户消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 4, request=request)
        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            'messages':messages,
        })

#登出
class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

#主页
class IndexView(View):
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        # courses =Course.objects.filter(is_banner=False)[:6]
        courses =Course.objects.all()[:3]
        # banner_courses = Course.objects.filter(is_banner=True)[:3]
        banner_courses = Course.objects.all()[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })

def pag_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
