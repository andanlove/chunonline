# _*_ encoding:utf-8 _*_

from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"课程机构")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"讲师")
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    category = models.CharField(default="全栈", max_length=20, verbose_name=u"课程类别", )
    detail =  UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",filePath="courses/ueditor/", default='')
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    knowledge = models.CharField(max_length=300, verbose_name=u"课程须知")
    learn_master = models.CharField(max_length=300, verbose_name=u"掌握知识")
    is_banner = models.CharField(max_length=5,choices=(('false','否'),('true','是')),verbose_name=u'是否轮播',default= 'false',null=True,blank=True)
    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_nums(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name
    get_zj_nums.short_description = '章节数'#后台显示


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True #防止在数据库生成表，直接引用Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加信息")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视屏名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）", null=True, blank=True)
    url = models.CharField(max_length=100, verbose_name=u"访问地址", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加信息")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to=u"course/resource/%Y/%m", verbose_name=u"下载", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加信息")

    class Meta:
        verbose_name = u"资源信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
