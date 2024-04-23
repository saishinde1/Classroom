from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    list_display=['username','user_type']
admin.site.register(CustomUser,UserModel)
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Teacher_leave)
admin.site.register(Student_Feedback)
admin.site.register(Student_Leave)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
<<<<<<< HEAD
admin.site.register(Assignment)
admin.site.register(Notice)
=======
admin.site.register(StudentResult)
>>>>>>> a63c055e995e75f19fa94ddf2d21f4e5577d0b7c
