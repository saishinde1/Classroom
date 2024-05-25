from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER=(
        (1,'HOD'),
        (2,'TEACHER'),
        (3,'STUDENT')
    )
    user_type=models.CharField(choices=USER, max_length=50,default=1)
    profile_pic=models.ImageField(upload_to='media/profile_pic/')
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Session_Year(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)


    def __str__(self):
        return self.session_start + " To " + self.session_end
    
class Student(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
    
class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.admin.username
    
class Subject(models.Model):
    name=models.CharField(max_length=100)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Teacher_leave(models.Model):
    teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    message=models.TextField()
    status=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.teacher_id.admin.first_name + self.teacher_id.admin.last_name
    
class Student_Feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(null=True, default="")
    status=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.student_id.admin.first_name + " " + self.student_id.admin.last_name
    
class Student_Leave(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    message=models.TextField()
    status=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.student_id.admin.first_name + self.student_id.admin.last_name

class Attendance(models.Model):
    subject_id=models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    session_year_id=models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_id.name
    
class Attendance_Report(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.admin.first_name

class StudentResult( models.Model ) :
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE)
    assignment_mark = models.IntegerField()
    exam_mark = models.IntegerField()
    total_marks = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.student_id.admin.first_name


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)  # Link assignment to a subject
    files = models.FileField(upload_to='media/assignments')  # File upload for the assignment

    def __str__(self):
        return self.title
    
class Submission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link submission to a student
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link submission to a course
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Link submission to a subject
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE) 
    status=models.IntegerField(default=0)
    submission_date = models.DateTimeField(auto_now_add=True)  # Submission date/time
    file = models.FileField(upload_to='media/submissions')  # File upload for the submission
    
    def __str__(self):
        return f"{self.student.username}'s submission for {self.assignment.title}"
    
 
class Notice(models.Model):
        course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
        description = models.TextField()
        date = models.DateField()


        def __str__(self):
            return f"{self.course.name} - {self.date}"


