from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserFavorite
from .foms import UserAskForm
from .models import CourseOrg, CityDict, Teacher


# Create your views here.

class OrgView(View):
    """
    机构主页
    """

    def get(self, request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()
        current_nav = "授课机构"
        # 机构排名
        hot_orgs = all_org.order_by("-click_nums")[:5]
        # 城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        # 类别筛选
        ct_id = request.GET.get('ct', "")
        if ct_id:
            all_org = all_org.filter(catgory=ct_id)
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_org = all_org.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        # 课程/学生排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_org = all_org.order_by("-students")
            elif sort == "courses":
                all_org = all_org.order_by("-cours_nums")
        # 统计课程数
        org_nums = all_org.count()
        # 课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, 4, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "orgs": orgs,
            "all_city": all_city,
            "org_nums": org_nums,
            "city_id": city_id,
            "ct_id": ct_id,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "current_nav": current_nav,
        })


class AddUserAskView(View):
    """
    用户咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构详情首页
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": "home",
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        has_fav = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": "course",
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        has_fav = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": "desc",
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        has_fav = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": "teacher",
            "has_fav": has_fav,
        })


class AddFavView(View):
    """
    用户收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            exist_record.delete()
            #收藏人数
            if int(fav_type) == 1:
                course = Course.objects.get(id = int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums<0:
                    course.fav_nums = 0
                    course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id = int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums<0:
                    org.fav_nums = 0
                    org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id = int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums<0:
                    teacher.fav_nums = 0
                    teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            #收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
            #收藏人数
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums += 1
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums += 1
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums += 1
                teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏失败"}', content_type='application/json')
