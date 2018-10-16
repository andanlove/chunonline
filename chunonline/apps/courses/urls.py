#_*_ coding: utf-8 _*_ 
__author__ = "andan"
__data__ = "2018/9/23 21:37"

from django.urls import path
from .views import CourseListView,CourseDetailView,LessonView,CommentView,AddCommentView,VideoView
from .views import TeacherListView,TeacherDetailView
app_name = "course"
urlpatterns = [
    path('list/',CourseListView.as_view(),name = "course_list"),
    path('detail/<int:course_id>/',CourseDetailView.as_view(),name = "course_detail"),
    path('lesson/<int:courses_id>/',LessonView.as_view(),name = "course_lesson"),
    path('comment/<int:courses_id>/',CommentView.as_view(),name = "course_comment"),
    path('add_coment/',AddCommentView.as_view(),name = "add_comment"),
    path('video/<int:video_id>/', VideoView.as_view(), name="course_video"),
    #授课教师
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    path('teacher/detail/<int:teacher_id>/', TeacherDetailView.as_view(), name="teacher_detail"),
]