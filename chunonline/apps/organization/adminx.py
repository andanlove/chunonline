#_*_ coding: utf-8 _*_ 
__author__ = "andan"
__data__ = "2018/9/18 10:38"

import xadmin
from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name']
    list_filter = ['name','desc','add_time']
    model_icon = 'fa fa-map-marker'


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name','desc','address','city']
    list_filter = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
    model_icon = 'fa fa-university'

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums','fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_year', 'work_company', 'work_position']
    list_filter = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums','fav_nums', 'add_time']
    model_icon = 'fa fa-graduation-cap'
    ordering = ['-click_nums']  # 排序
    readonly_fields = ['click_nums']  # 只读字段，不能编辑
    exclude = ['fav_nums']  # 不显示的字段

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)