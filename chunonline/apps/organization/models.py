# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models


# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市信息")
    desc = models.TextField(verbose_name=u"城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    catgory = models.CharField(verbose_name=u"机构类别", max_length=20,
                               choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")), default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u"所在城市")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    cours_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    # tag = models.CharField('机构标签',max_length=10,default=u'全国知名',null=True,blank=True)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_year = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"入职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击人数")
    age = models.IntegerField(default=0, verbose_name=u"教师年龄",null=True, blank=True)
    image = models.ImageField(upload_to="Tea/%Y/%m", verbose_name=u"头像", max_length=100, null=True, blank=True)
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def get_course_nums(self):
        self.course_set.all().count()


    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
