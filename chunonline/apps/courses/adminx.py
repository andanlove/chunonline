# _*_ coding: utf-8 _*_
__author__ = "andan"
__data__ = "2018/9/18 9:07"

import xadmin
from .models import Course, Lesson, Video, CourseResource,BannerCourse

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']
    model_icon = 'fa fa-bookmark'



class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']

    model_icon = 'fa fa-youtube-play'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'download', 'add_time']
    model_icon = 'fa fa-file'


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','get_zj_nums', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']

    model_icon = 'fa fa-book'
    ordering = ['-click_nums']  # 排序
    readonly_fields = ['click_nums']  # 只读字段，不能编辑
    exclude = ['fav_nums']  # 不显示的字段
    inlines = [LessonInline, CourseResourceInline]  # 增加章节和课程资源
    list_editable = ['degree', 'desc']#直接在页面修改
    refresh_times = [3,5]
    style_fields = {"detail": "ueditor"}


    def queryset(self):
        # 重载queryset的方法，过滤数据
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner = 'false')
        return qs


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']

    model_icon = 'fa fa-book'
    ordering = ['-click_nums']  # 排序
    readonly_fields = ['click_nums']  # 只读字段，不能编辑
    exclude = ['fav_nums']  # 不显示的字段

    def queryset(self):
        # 重载queryset的方法，过滤数据
        qs = super( BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner='true')
        return qs





xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
