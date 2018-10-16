# _*_ coding: utf-8 _*_
__author__ = "andan"
__data__ = "2018/9/22 13:11"

from django.urls import path

from .views import UserInfoView, UploadImageView, UpdatePwdView,SendEmailCodeView,UpdateEmailView
from .views import User_login, Register, ActiveUserView, ForgetPwdView, ResetUserView, ModifyView
from .views import MyCourseView,MyFavOrg,MyFavCourse,MyFavTeacher,MyMessageView,LogoutView

app_name = "user"

urlpatterns = [
    path('login/', User_login.as_view(), name="login"),
    path('register/', Register.as_view(), name="register"),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name="forget"),
    path('reset/<active_code>/', ResetUserView.as_view(), name="reset"),
    path('modify/', ModifyView.as_view(), name="modify"),

    # 用户信息
    path('userinfo/', UserInfoView.as_view(), name="userinfo"),
    # 头像上传
    path('image_upload/', UploadImageView.as_view(), name="imgupload"),
    # 用户个人中心修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name="updeate_pwd"),
    # 修改邮箱
    path('sendemail_code/',SendEmailCodeView.as_view(), name="sendemail_code"),
    #修改邮箱验证
    path('update_email/',UpdateEmailView.as_view(), name="update_email"),
    #我的课程
    path('mycourse/',MyCourseView.as_view(),name = "mycourse"),
    #我的收藏-机构
    path('myfav/org/',MyFavOrg.as_view(),name = "myfav_org"),
    #我的收藏-课程
    path('myfav/course/',MyFavCourse.as_view(),name = "myfav_course"),
    #我的收藏-教师
    path('myfav/teacher/',MyFavTeacher.as_view(),name = "myfav_teacher"),
    #我的消息
    path('my_message/',MyMessageView.as_view(),name = "my_message"),
    #登出
    path('logout/', LogoutView.as_view(), name="logout"),


]
