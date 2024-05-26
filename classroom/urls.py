"""classroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import teacher_Views, views,hod_Views,student_Views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.divya,name='base'),
    path('',views.LOGIN,name='login'),
    path('dologin',views.dologin,name='dologin'),
    path('dologout',views.dologout,name='logout'),
    path('profile/', views.PROFILE,name='profile'),
    path('profile/update',views.PROFILE_UPDATE,name='profile_update'),
    
    path('hod/home',hod_Views.home,name='hod_home'),
    path('hod/student/add',hod_Views.ADD_STUDENT,name='add_student'),
    path('Hod/Student/View',hod_Views.VIEW_STUDENT,name='view_student'),
    path('Hod/Student/Edit/<str:id>',hod_Views.EDIT_STUDENT,name='edit_student'),
    path('Hod/Student/Update',hod_Views.UPDATE_STUDENT,name='update_student'),
    path('Hod/Student/Delete/<str:admin>',hod_Views.DELETE_STUDENT,name='delete_student'),
    
    path('Hod/Student/Feedback',hod_Views.STUDENT_FEEDBACK,name='get_student_feedback'),
    path('Hod/Student/Feedback/save',hod_Views.STUDENT_FEEDBACK_SAVE,name='student_feedback_reply_save'),


    path('Hod/Course/Add',hod_Views.ADD_COURSE,name='add_course'),
    path('Hod/Course/View',hod_Views.VIEW_COURSE,name='view_course'),
    path('Hod/Course/Edit/<str:id>',hod_Views.EDIT_COURSE,name='edit_course'),
    path('Hod/Course/Update',hod_Views.UPDATE_COURSE,name='update_course'),
    path('Hod/Course/Delete/<str:id>',hod_Views.DELETE_COURSE,name='delete_course'),
    
    path('Hod/Teacher/Add', hod_Views.ADD_TEACHER,name='add_teacher'),
    path('Hod/Teacher/View', hod_Views.VIEW_TEACHER,name='view_teacher'),
    path('Hod/Teacher/Edit/<str:id>', hod_Views.EDIT_TEACHER,name='edit_teacher'),
    path('Hod/Teacher/Update', hod_Views.UPDATE_TEACHER,name='update_teacher'),
    path('Hod/Teacher/Delete/<str:admin>',hod_Views.DELETE_TEACHER,name='delete_teacher'),

    path('Hod/Subject/Add', hod_Views.ADD_SUBJECT, name='add_subject'),
    path('Hod/Subject/View', hod_Views.VIEW_SUBJECT,name='view_subject'),
    path('Hod/Subject/Edit/<str:id>', hod_Views.EDIT_SUBJECT,name='edit_subject'),
    path('Hod/Subject/Update', hod_Views.UPDATE_SUBJECT,name='update_subject'),
    path('Hod/Subject/Delete/<str:id>',hod_Views.DELETE_SUBJECT,name='delete_subject'),
    
   
    path('Hod/Session/Add', hod_Views.ADD_SESSION, name='add_session'),
    path('Hod/Session/View', hod_Views.VIEW_SESSION,name='view_session'),
    path('Hod/Session/Edit/<str:id>', hod_Views.EDIT_SESSION,name='edit_session'),
    path('Hod/Session/Update', hod_Views.UPDATE_SESSION,name='update_session'),
    path('Hod/Session/Delete/<str:id>',hod_Views.DELETE_SESSION,name='delete_session'),
    
    path('Hod/Teacher/Leave_view',hod_Views.TEACHER_LEAVE_VIEW,name='teacher_leave_view'),
    path('Hod/Teacher/Approve_leave/<str:id>',hod_Views.TEACHER_APPROVE_LEAVE,name='teacher_approve_leave'),
    path('Hod/Teacher/Disapprove_leave/<str:id>',hod_Views.TEACHER_DISAPPROVE_LEAVE,name='teacher_disapprove_leave'),

    path('Hod/Student/Leave_view',hod_Views.STUDENT_LEAVE_VIEW,name='student_leave_view'),
    path('Hod/Student/Approve_leave/<str:id>',hod_Views.STUDENT_APPROVE_LEAVE,name='student_approve_leave'),
    path('Hod/Student/Disapprove_leave/<str:id>',hod_Views.STUDENT_DISAPPROVE_LEAVE,name='student_disapprove_leave'),

    path('Hod/View_attendace',hod_Views.HOD_VIEW_ATTENDANCE,name='hod_view_attendance'),
    path('Hod/upload_notice',hod_Views.HOD_UPLOAD_NOTICE,name='hod_upload_notice'),
    path('Hod/view_notice',hod_Views.HOD_VIEW_NOTICE,name='hod_view_notice'),

    
   
    #this is for teacher

    path('Teacher/home',teacher_Views.HOME,name='teacher_home'),
    path('Teacher/student/add',teacher_Views.teach_ADD_STUDENT,name='teach_add_student'),
    path('Teacher/Student/View',teacher_Views.teach_VIEW_STUDENT,name='teach_view_student'),
    path('Teacher/Student/Edit/<str:id>',teacher_Views.teach_EDIT_STUDENT,name='teach_edit_student'),
    path('Teacher/Student/Update',teacher_Views.teach_UPDATE_STUDENT,name='teach_update_student'),
    path('Teacher/Student/Delete/<str:admin>',teacher_Views.teach_DELETE_STUDENT,name='teach_delete_student'),

    path('Teacher/Apply_leave',teacher_Views.TEACHER_APPLY_LEAVE,name='teacher_apply_leave'),
    path('Teacher/Apply_leave_save',teacher_Views.TEACHER_APPLY_LEAVE_SAVE,name='teacher_apply_leave_save'),

    path('Teacher/Take_attendace',teacher_Views.TEACHER_TAKE_ATTENDANCE,name='teacher_take_attendance'),
    path('Teacher/Save_attendace',teacher_Views.TEACHER_SAVE_ATTENDANCE,name='teacher_save_attendance'),
    path('Teacher/View_attendace',teacher_Views.TEACHER_VIEW_ATTENDANCE,name='teacher_view_attendance'),

    path('Teacher/send_Assignment',teacher_Views.teacher_send_assignment,name='teacher_send_assignment'),
    path('Teacher/View_Assignment',teacher_Views.TEACHER_VIEW_ASSIGNMENT,name='teacher_view_assignment'),
    path('Teacher/delete_Assignment/<str:id>',teacher_Views.TEACHER_DELETE_ASSIGNMENT,name='teacher_delete_assignment'),
    
    path('Teacher/View_submission',teacher_Views.TEACHER_VIEW_SUBMISSION,name='teacher_view_submission'),

    path('Teacher/add/Result',teacher_Views.TEACHER_ADD_RESULT,name='teacher_add_result'),
    path('Teacher/save/Result',teacher_Views.TEACHER_SAVE_RESULT,name='teacher_save_result'),

    path('Teacher/View_notice',teacher_Views.TEACHER_VIEW_NOTICE,name='teacher_view_notice'),

    
    #this is for Student
    path('Student/home',student_Views.HOME,name='student_home'),
    
    path('Student/feedback',student_Views.STUDENT_FEEDBACK,name='student_feedback'),
    path('Student/feedback/save',student_Views.STUDENT_FEEDBACK_SAVE,name='student_feedback_save'),

    path('Student/Apply_for_leave',student_Views.STUDENT_LEAVE,name='student_leave'),
    path('Student/leave_save',student_Views.STUDENT_LEAVE_SAVE,name='student_leave_save'),
    
    path('Student/View_attendace',student_Views.STUDENT_VIEW_ATTENDANCE,name='student_view_attendance'),
    path('Student/View_Result',student_Views.STUDENT_VIEW_RESULT,name='student_view_result'),
    path('Student/View_notice',student_Views.STUDENT_VIEW_NOTICE,name='student_view_notice'),
    path('Student/View_Assignment',student_Views.STUDENT_VIEW_ASSIGNMENT,name='student_view_assignment'),
    path('Student/Complete_Assignment/<str:id>',student_Views.STUDENT_COMPLETE_ASSIGNMENT,name='student_complete_assignment'),
    path('Student/Save_Assignment',student_Views.STUDENT_SAVE_ASSIGNMENT,name='student_save_assignment'),

   

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
