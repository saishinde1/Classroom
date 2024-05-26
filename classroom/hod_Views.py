from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from students.models import Course,Session_Year,CustomUser,Student,Teacher,Subject,Teacher_leave,Student_Feedback,Student_Leave,Attendance,Attendance_Report,Notice,StudentResult
from django.contrib import messages
from itertools import chain


def calculate_percentage(total_marks):
    total_marks_possible = 75
    percentage = (total_marks / total_marks_possible) * 100
    rounded_percentage = round(percentage, 2)  # Round to 2 decimal places
    return rounded_percentage

@login_required(login_url='/')
def home(request):

    student_count = Student.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    above50 = StudentResult.objects.filter(total_marks__gte=50).count()
    below24 = StudentResult.objects.filter(total_marks__lte=24).count()
    passed = StudentResult.objects.filter(total_marks__gte=25).count()

    print(above50,below24,passed)
    courses = Course.objects.all()

    # Fetch top 3 students for each course dynamically
    all_top_students = []
    for course in courses:
        top_students = StudentResult.objects.filter(
            student_id__course_id=course
        ).order_by('-total_marks')[:3]

        all_top_students.extend(list(top_students))

    # Calculate percentage for each student
    for student in all_top_students:
        student.percentage = calculate_percentage(student.total_marks)
    print(all_top_students)

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'student_gender_female': student_gender_female,
        'student_gender_male': student_gender_male,
        'above50': above50,
        'below24': below24,
        'passed': passed,
        'all_top_students':all_top_students
    }

    return render(request, 'hod/home.html', context)


@login_required(login_url='/')
def ADD_STUDENT(request):
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
           return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('add_student')
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
            return redirect('add_student')



    context = {
        'course':course,
        'session_year':session_year,
    }

    return render(request,'Hod/add_student.html',context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()

    context = {
        'student':student,
    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student':student,
        'course':course,
        'session_year':session_year,
    }
    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
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
        return redirect('view_student')

    return render(request,'hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):

    if request.method == "POST":
        course_name = request.POST.get('course_name')

        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request,'Course Are Successfully Created ')

        # engine.say("course are successfully added")

        # engine.runAndWait()
        # engine.endLoop()
        return redirect('view_course')

    return render(request,'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request,'hod/view_course.html',context)
	
def EDIT_COURSE(request,id):
    course=Course.objects.get(id = id)
    context={
        'course':course
    }
    return render(request,'hod/edit_course.html',context)

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request,'Course are Successfully Deleted')

    return redirect('view_course')

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name=request.POST.get('name')
        course_id=request.POST.get('course_id')
        
        course=Course.objects.get(id = course_id)
        course.name=name
        course.save()
        messages.success(request,'course are successfully updated.')
        return redirect('view_course')
    return render(request,'hod/edit_course.html')

@login_required(login_url='/')
def ADD_TEACHER(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        
        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('add_teacher')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('add_teacher')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2
            )
            user.set_password(password)
            user.save()
            print(user)

            teacher = Teacher(
                admin = user,
                address = address,
                gender = gender,
            )
            teacher.save()
            messages.success(request, " Teacher is Successfully Added !")
            return redirect('add_teacher')


    return render(request,'hod/add_teacher.html')

@login_required(login_url='/')
def VIEW_TEACHER(request):
    teacher=Teacher.objects.all()
    
    context = {
        'teacher':teacher,

    }
    
    return render(request,'hod/view_teacher.html',context)

@login_required(login_url='/')
def EDIT_TEACHER(request,id):
    teacher = Teacher.objects.filter(id = id)
    context = {
        'teacher':teacher,
           }
    print(teacher)
    return render(request,'hod/edit_teacher.html',context)

@login_required(login_url='/')
def UPDATE_TEACHER(request):


    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        print(teacher_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        
        user = CustomUser.objects.get(id = teacher_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        teacher = Teacher.objects.get(admin = teacher_id)
        teacher.address = address
        teacher.gender = gender

     
        teacher.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_teacher')

    
    return render(request,'hod/edit_teacher.html')

@login_required(login_url='/')
def DELETE_TEACHER(request,admin):
    teacher = CustomUser.objects.get(id = admin)
    teacher.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_teacher')

@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    teacher= Teacher.objects.all()
    context = {
        'course':course,
        'teacher':teacher,
    }

    if request.method == "POST":
        
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        
        course = Course.objects.get(id=course_id)
        teacher = Teacher.objects.get(id=teacher_id)

        
        subject = Subject(
                name = subject_name,
                course = course,
                teacher= teacher,
               
        )
        
        subject.save()
        messages.success(request,'Subject is Successfully saved ')

    return render(request,'hod/add_subject.html',context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject=Subject.objects.all()
    context = {
        'subject':subject,
    }
    
    return render(request,'hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    teacher= Teacher.objects.all()
    context = {
        'subject':subject,
        'course':course,
        'teacher':teacher,
           }
    
    return render(request,'hod/edit_subject.html',context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request):


    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        
        course = Course.objects.get(id = course_id)
        teacher = Teacher.objects.get(id = teacher_id)
        
        subject = Subject(
                id=subject_id,
                name = subject_name,
                course = course,
                teacher= teacher,
               
        )
     
        subject.save()
        messages.success(request,'subject is Successfully Updated !')
        return redirect('view_subject')

@login_required(login_url='/')
def DELETE_SUBJECT(request,id):
    subject = Subject.objects.filter(id = id)
    subject.delete()
    messages.success(request,'subject is Successfully Deleted !')
    return redirect('view_subject')

@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')
       
        session=Session_Year(
           session_start= session_year_start,
           session_end= session_year_end,
        )
        session.save()
        messages.success(request, " Session is Successfully Added !")
        return redirect('add_session')


    return render(request,'hod/add_session.html')

@login_required(login_url='/')
def VIEW_SESSION(request):
    session=Session_Year.objects.all()
    context = {
        'session':session,
    }
    
    return render(request,'hod/view_session.html',context)

@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session= Session_Year.objects.filter(id=id)
    context = {
        'session':session,
           }
    
    return render(request,'hod/edit_session.html',context)

@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session=Session_Year(
            id=session_id,
            session_start=session_year_start,
            session_end=session_year_end,
        )

        session.save()
        messages.success(request,'session is Successfully Updated !')
        return redirect('view_session')

    
@login_required(login_url='/')
def DELETE_SESSION(request,id):
    session = Session_Year.objects.get(id = id)
    session.delete()
    messages.success(request,'session is Successfully Deleted !')
    return redirect('view_session')

def TEACHER_LEAVE_VIEW(request):
    teacher_leave = Teacher_leave.objects.all()
    context = {
        'teacher_leave':teacher_leave,
    }
    return render(request,'hod/teacher_leave.html',context)

def TEACHER_APPROVE_LEAVE(request,id):
    
    leave = Teacher_leave.objects.get(id = id)
    leave.status=1
    leave.save()
    return redirect('teacher_leave_view')

def TEACHER_DISAPPROVE_LEAVE(request,id):

    leave = Teacher_leave.objects.get(id = id)
    leave.status=2
    leave.save()
    return redirect('teacher_leave_view')

def STUDENT_FEEDBACK(request):

    feedback=Student_Feedback.objects.all()
    feedback_history=Student_Feedback.objects.all().order_by('-id')[0:5]
    context={
        'feedback':feedback,
        'feedback_history':feedback_history,
    }

    return render(request,'hod/student_feedback.html',context)

def STUDENT_FEEDBACK_SAVE(request):

    if request.method== 'POST':
        feedback_id=request.POST.get('feedback_id')
        feedback_reply=request.POST.get('feedback_reply')
    
    feedback=Student_Feedback.objects.get(id=feedback_id)
    feedback.feedback_reply=feedback_reply
    feedback.status=1
    feedback.save()
    return redirect('get_student_feedback')

def STUDENT_LEAVE_VIEW(request):
    student_leave=Student_Leave.objects.all()
    context={
        'student_leave':student_leave,
    }
    return render(request,'hod/student_leave.html',context)
    
def STUDENT_APPROVE_LEAVE(request,id):
    
    leave = Student_Leave.objects.get(id = id)
    leave.status=1
    leave.save()
    return redirect('student_leave_view')

def STUDENT_DISAPPROVE_LEAVE(request,id):

    leave = Student_Leave.objects.get(id = id)
    leave.status=2
    leave.save()
    return redirect('student_leave_view')

def HOD_VIEW_ATTENDANCE(request):
    subject=Subject.objects.all()
    session_year=Session_Year.objects.all()

    action=request.GET.get('action')

    get_subject=None
    get_session_year=None
    attendance=None
    attendance_report=None
    attendance_date=None

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
    return render(request,'hod/view_attendance.html',context)

def HOD_UPLOAD_NOTICE(request):
    course = Course.objects.all()
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        description = request.POST.get('description')
        date = request.POST.get('notice_date')
        coursee = Course.objects.get(id=course_id)
        notice = Notice(
                course = coursee,
                date = date,
                description = description,
            )
        notice.save()
        messages.success(request,"Successfully Posted !")
        return redirect('hod_view_notice')
    context = {
        'course':course,
        
    }
    return render(request,'hod/upload_notice.html',context)

def HOD_VIEW_NOTICE(request):
    Notice_history = Notice.objects.all()
    context = {
        'Notice_history':Notice_history,
    }
    return render(request,'hod/upload_notice.html',context)

