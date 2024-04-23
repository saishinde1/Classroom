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
from .import views,hod_Views,staff_views,student_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.divya,name='base'),
    path('',views.login,name='login'),
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
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
