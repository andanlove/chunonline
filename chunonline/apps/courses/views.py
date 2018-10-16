from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from operation.models import UserFavorite, Coursecomments, UserCourse
from .models import Course, CourseResource,Video,Teacher
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    def get(self, request):
        current_nav = "公开课"
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        sort = request.GET.get('sort', "")
        search_keywords = request.GET.get("keywords","")
        if search_keywords :
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__contains=search_keywords))
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)
        orgs = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': orgs,
            'sort': sort,
            'hot_courses': hot_courses,
            "current_nav":current_nav,
        })


class CourseDetailView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        courses = Course.objects.get(id=int(course_id))
        courses.click_nums += 1
        courses.save()
        #用户与课程进行关联
        user_course = UserCourse.objects.filter(course=courses)
        if not user_course:
            user_course = UserCourse(user=request.user,course=courses)
            user_course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.course_org.id, fav_type=2):
                has_fav_org = True

        relate_course = []
        tag = courses.tag
        if tag:
            tcourse = Course.objects.filter(tag=tag).order_by("-click_nums")
            for t in tcourse:
                if t.id != int(course_id):
                    relate_course.append(t)
                    break
        return render(request, 'course-detail.html', {
            'courses': courses,
            'relate_course': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class LessonView(LoginRequiredMixin,View):
    def get(self, request, courses_id):
        courses = Course.objects.get(id=int(courses_id))
        all_resouce = CourseResource.objects.filter(course=courses)
        # courses.students += 1
        # courses.save()
        user_courses = UserCourse.objects.filter(course=courses)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 选出所有选修这门课程的同学
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        # 取出学过该课程的同学学过的其他的课程
        relate_course = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        return render(request, 'course-video.html', {
            'courses': courses,
            'all_resouce': all_resouce,
            'relate_course':relate_course,
        })


class CommentView(View):
    def get(self, request, courses_id):
        courses = Course.objects.get(id=int(courses_id))
        all_comment = Coursecomments.objects.all()
        user_courses = UserCourse.objects.filter(course = courses)
        user_ids = [user_course.user.id for user_course in user_courses]
        #选出所有选修这门课程的同学
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        #取出学过该课程的同学学过的其他的课程
        relate_course = Course.objects.filter(id__in = course_ids).order_by("-click_nums")[:5]

        return render(request, 'course-comment.html', {
            'courses': courses,
            'all_comment': all_comment,
            'relate_course':relate_course,
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        courese_id = request.POST.get("course_id", "")
        comments = request.POST.get("comments", "")
        if int(courese_id) > 0 and comments:
            course_coments = Coursecomments()
            try:
                courese = Course.objects.get(id=courese_id)
            except:
                courese = None
            course_coments.course = courese
            course_coments.comments = comments
            course_coments.user = request.user
            course_coments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')



class VideoView(View):
    '''
    视频播放页面
    '''
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        relate_course = []
        tag = course.tag
        if tag:
            tcourse = Course.objects.filter(tag=tag).order_by("-click_nums")
            for t in tcourse:
                if t.id != int(video_id):
                    relate_course.append(t)
                    break
        return render(request, 'course-play.html', {
            'course': course,
            'video':video,
            'relate_course': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class TeacherListView(View):
    '''
    课程讲师列表
    '''
    def get(self,request):
        current_nav = "授课教师"
        all_teachers = Teacher.objects.all()
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) | Q(points__icontains=search_keywords)|Q(work_company__icontains=search_keywords))
        sort = request.GET.get("sort","")
        teacher_nums = all_teachers.count()
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        #教师分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 4, request=request)
        teachers = p.page(page)
        return render(request,'teachers-list.html',{
            'teachers':teachers,
            'sorted_teachers':sorted_teachers,
            'sort':sort,
            'teacher_nums':teacher_nums,
            'current_nav':current_nav,
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id = teacher_id)
        all_course = teacher.course_set.filter(teacher=teacher)
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        org = teacher.org
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
        return render(request,"teacher-detail.html",{
            'teacher':teacher,
            'all_course':all_course,
            "sorted_teachers":sorted_teachers,
            "org":org,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })