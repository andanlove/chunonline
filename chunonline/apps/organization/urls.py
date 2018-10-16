#_*_ coding: utf-8 _*_ 
__author__ = "andan"
__data__ = "2018/9/22 12:48"
from django.urls import path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView,OrgDescView,OrgTeacherView,AddFavView

app_name = "org"
urlpatterns = [
    # 课程
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_ask/',AddUserAskView.as_view(),name="add_ask"),
    path('orghome/<int:org_id>',OrgHomeView.as_view(),name="orghome"),
    path('orgcourse/<int:org_id>',OrgCourseView.as_view(),name="orgcourse"),
    path('orgdesc/<int:org_id>',OrgDescView.as_view(),name="orgdesc"),
    path('orgteacher/<int:org_id>',OrgTeacherView.as_view(),name="orgteacher"),

    #机构收藏
    path('add_fav/',AddFavView.as_view(),name="add_fav"),
]