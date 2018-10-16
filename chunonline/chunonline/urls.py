"""chunonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.static import serve

import xadmin
from chunonline.settings import MEDIA_ROOT
from users.views import IndexView

urlpatterns = [
    # 后台页面
    path('xadmin/', xadmin.site.urls),
    # 主页
    path('', IndexView.as_view(), name="index"),
    # 分页
    path('captcha/', include('captcha.urls')),
    # 课程机构信息
    path('org/', include('organization.urls', namespace="org")),
    # 登录注册
    path('user/', include('users.urls', namespace="user")),
    # 课程信息
    re_path('^course/', include('courses.urls', namespace="course")),
    #富文本编辑
    path('ueditor/',include('DjangoUeditor.urls')),
    # 配置上传文件的访问处理
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),

]
#404页面
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'