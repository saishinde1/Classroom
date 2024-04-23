from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from students.models import Course,Session_Year,CustomUser,Student,Teacher,Subject,Teacher_leave,Attendance,Attendance_Report,Assignment
=======
from students.models import Course,Session_Year,CustomUser,Student,Teacher,Subject,Teacher_leave,Attendance,Attendance_Report,StudentResult
>>>>>>> a63c055e995e75f19fa94ddf2d21f4e5577d0b7c
from django.contrib import messages

from django.utils.dateparse import parse_datetime

@login_required(login_url='/')
def HOME(request):
    user = request.session.get('user')
    return render(request, 'Teacher/home.html')

def teach_ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('teach_add_student')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('teach_add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()
            
            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin = user,
                address = address,
                session_year_id = session_year,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Are Successfully Added !")
            return redirect('teach_add_student')



    context = {
        'course':course,
        'session_year':session_year,
    }

    return render(request,'Teacher/add_student.html',context)

@login_required(login_url='/')
def teach_VIEW_STUDENT(request):
    student = Student.objects.all()

    context = {
        'student':student,
    }
    return render(request,'Teacher/view_student.html',context)

@login_required(login_url='/')
def teach_EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student':student,
        'course':course,
        'session_year':session_year,
    }
    return render(request,'Teacher/edit_student.html',context)

@login_required(login_url='/')
def teach_UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        print(student_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id = course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('teach_view_student')

    return render(request,'Teacher/edit_student.html')

@login_required(login_url='/')
def teach_DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('teach_view_student')


def TEACHER_APPLY_LEAVE(request):
    teacher=Teacher.objects.filter(admin=request.user.id)
    for i in teacher:
        teacher_id=i.id
        leave_history=Teacher_leave.objects.filter(teacher_id=teacher_id)
        context={
            'leave_history':leave_history
        }
        return render(request,'Teacher/apply_leave.html',context)

def TEACHER_APPLY_LEAVE_SAVE(request):
    if request.method=="POST":
        leave_date=request.POST.get('leave_date')
        leave_message=request.POST.get('leave_message')

        teacher=Teacher.objects.get(admin=request.user.id)


        leave=Teacher_leave(
         teacher_id=teacher,
         date=leave_date,
         message=leave_message,
         
        )
        leave.save()
        messages.success(request,"Successfully Applied for Leave")
    
    return redirect('teacher_apply_leave')


def TEACHER_TAKE_ATTENDANCE(request):
    teacher_id=Teacher.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(teacher_id=teacher_id)
    session_year=Session_Year.objects.all()
    students=None
    get_subject = None  # Initialize get_subject
    get_session_year = None

    action=request.GET.get('action')
    if action is not None:
        if request.method== "POST":
            subject_id=request.POST.get('subject_id')
            session_year_id=request.POST.get('session_year_id')

            get_subject=Subject.objects.get(id=subject_id)
            get_session_year=Session_Year.objects.get(id=session_year_id)
            
            subject=Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id=i.course.id
                students=Student.objects.filter(course_id=student_id)

            
           
    context={
        'subject':subject,
        'session_year':session_year,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'action':action,
        'students':students,
    }

    return render(request,'Teacher/take_attendance.html',context)

def TEACHER_SAVE_ATTENDANCE(request):

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_ids = request.POST.getlist('student_id')  # Renamed to student_ids for clarity

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year
        )
        attendance.save()

        print(request.POST)

        for stud_id in student_ids:
            int_stud = int(stud_id)
            print(int_stud)
            p_student = Student.objects.get(id=int_stud)  # Renamed to p_student for clarity
            attendance_report = Attendance_Report(
                student_id=p_student,
                attendance_id=attendance,
            )
            attendance_report.save()

    return redirect('teacher_take_attendance')


def TEACHER_VIEW_ATTENDANCE(request):
    teacher_id=Teacher.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(teacher_id=teacher_id)
    session_year=Session_Year.objects.all()

    action=request.GET.get('action')

<<<<<<< HEAD
    get_subject= None
    get_session_year= None
    attendance_date= None
    attendance_report= None
=======
    get_subject=None
    get_session_year=None
    attendance_date=None
    attendance_report=None
    attendance_date=None
>>>>>>> a63c055e995e75f19fa94ddf2d21f4e5577d0b7c

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date=request.POST.get('attendance_date')

            get_subject=Subject.objects.get(id=subject_id)
            get_session_year=Session_Year.objects.get(id=session_year_id)
            attendance=Attendance.objects.filter(subject_id=get_subject,attendance_date=attendance_date)

            for i in attendance:
                attendance_id=i.id
                attendance_report=Attendance_Report.objects.filter(attendance_id=attendance_id)



    context={
        'subject':subject,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'attendance_date':attendance_date,
        'attendance_report':attendance_report

    }

    return render(request,'Teacher/view_attendance.html',context)

<<<<<<< HEAD
@login_required(login_url='/')
def teacher_send_assignment(request):
    teacher_id=Teacher.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(teacher_id=teacher_id)
    get_subject = None 
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('submission_date')
        file = request.FILES.get('upload_file')
        subject_id = request.POST.get('subject_id')
        get_subject=Subject.objects.get(id=subject_id)
         
   
        assignment=Assignment(
            title=title,
            description=description,
            deadline=deadline,
            subject_id=get_subject,
            file=file
            )
    
        assignment.save()
        messages.success(request,"Successfully Created")
        return redirect('teacher_send_assignment')

    context={
        'subject':subject,
       
    }
    
    return render(request,'Teacher/send_assignment.html',context)
=======
def TEACHER_SEND_ASSIGNMENT(request):
    return render(request,'Teacher/send_assignment.html')

def TEACHER_ADD_RESULT(request):
    teacher = Teacher.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(teacher_id = teacher)
    print(subjects)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
           subject_id = request.POST.get('subject_id')
           session_year_id = request.POST.get('session_year_id')

           get_subject = Subject.objects.get(id = subject_id)
           get_session = Session_Year.objects.get(id = session_year_id)
 
           subjects = Subject.objects.filter(id = subject_id)
           for i in subjects:
               student_id = i.course.id
               students = Student.objects.filter(course_id = student_id)


    context = {
        'subjects':subjects,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,
    }

    return render(request,'Teacher/add_result.html',context)

def TEACHER_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.subject_assignment_marks = assignment_mark
            result.subject_exam_marks = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('teacher_add_result')
        else:
            result = StudentResult(
                student_id=get_student, 
                subject_id=get_subject, 
                exam_mark=Exam_mark,
                assignment_mark=assignment_mark
                )
            
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('teacher_add_result')
        

>>>>>>> a63c055e995e75f19fa94ddf2d21f4e5577d0b7c
