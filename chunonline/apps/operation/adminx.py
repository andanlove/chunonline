#_*_ coding: utf-8 _*_
__author__ = "andan"
__data__ = "2018/9/18 10:37"

import xadmin
from .models import UserAsk,Coursecomments,UserFavorite,UserMessage,UserCourse

class UserAskAdmin(object):
    list_display = ['name','moblie','course_name','add_time']
    search_fields = ['name','course_name']
    list_filter = ['name','moblie','course_name','add_time']
    model_icon = 'fa fa-volume-up'

class CoursecommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'comments', 'add_time']
    model_icon = 'fa fa-comments'

class  UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user',]
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-heart'


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    model_icon = 'fa fa-commenting'


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user','course']
    list_filter = ['user', 'course', 'add_time']
    model_icon = 'fa fa-wpforms'


xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(Coursecomments,CoursecommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
