from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from students.models import Course,Session_Year,CustomUser,Student,Teacher,Subject,Teacher_leave,Student_Feedback,Student_Leave,Attendance,Attendance_Report,StudentResult,Notice,Assignment,Submission
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):

    user = request.session.get('user')
    student_id=Student.objects.get(admin=request.user.id)
    student= Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course_id=student.course_id)
    subject_count = subjects.count()

    # Fetch the distinct teachers for these subjects
    teacher_ids = subjects.values_list('teacher_id', flat=True).distinct()
    teacher_count = Teacher.objects.filter(id__in=teacher_ids).count()
    
    assignments = Assignment.objects.filter(subject_id__in=subjects.values_list('id', flat=True))

    # Get all submissions made by the student
    submissions = Submission.objects.filter(student_id=student.admin_id, assignment_id__in=assignments.values_list('id', flat=True))

    # Determine pending assignments
    submitted_assignment_ids = submissions.values_list('assignment_id', flat=True)
    pending_assignments_count = assignments.exclude(id__in=submitted_assignment_ids).count()
    submitted_assignments_count = submissions.count()  # Count the submitted assignments

    results = StudentResult.objects.filter(student_id=student.id)
    # Define passing marks
    passing_marks = 30

    # Calculate passed and failed subjects
    passed_subjects_count = results.filter(total_marks__gte=passing_marks).count()
    failed_subjects_count = results.filter(total_marks__lt=passing_marks).count()

    # Pass the statistics to the template
    context = {
        'subject_count': subject_count,
        'teacher_count': teacher_count,
        'pending_assignments_count':pending_assignments_count,
        'submitted_assignments_count':submitted_assignments_count,
        'passed_subjects_count': passed_subjects_count,
        'failed_subjects_count': failed_subjects_count,
        'results':results
    }
    return render(request, 'Student/home.html',context)

def STUDENT_FEEDBACK(request):

    student_id= Student.objects.get(admin=request.user.id)
    feedback_history=Student_Feedback.objects.filter(student_id=student_id)

    context={
        "feedback_history":feedback_history
    }

    return render(request,'Student/feedback.html',context)


def STUDENT_FEEDBACK_SAVE(request):

    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student_id= Student.objects.get(admin=request.user.id)

        feed=Student_Feedback(
            student_id=student_id,
            feedback=feedback,
            
            )
        feed.save()
        messages.success(request, "Feedback Sent.")
        return redirect('student_feedback')
    
def STUDENT_LEAVE(request):
    student=Student.objects.filter(admin=request.user.id)
    for i in student:
        student=i.id
        leave_history=Student_Leave.objects.filter(student_id=student)
        context={
            'leave_history':leave_history
        }
        return render(request,'Student/apply_leave.html',context)

def STUDENT_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date=request.POST.get('leave_date')
        leave_message=request.POST.get('leave_message')

        student_id= Student.objects.get(admin=request.user.id)
        leave=Student_Leave(
            student_id=student_id,
            date=leave_date,
            message=leave_message,
            
        )
        leave.save()
        messages.success(request, "Applied for Leave.")
        return redirect('student_leave')
    
def STUDENT_VIEW_ATTENDANCE(request):

    student= Student.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(course_id=student.course_id)
    action=request.GET.get('action')

    get_subject= None
    attendance_report= None

    if action is not None:
        if request.method == "POST":
            subject_id=request.POST.get('subject_id')
            get_subject=Subject.objects.get(id=subject_id)
            attendance_report=Attendance_Report.objects.filter(attendance_id__subject_id=subject_id,student_id=student)
    context={
        'subject':subject,
        'action':action,
        'attendance_report':attendance_report,
        'get_subject':get_subject,
    }
    return render(request,'Student/view_attendance.html',context)


def STUDENT_VIEW_RESULT(request):
    student= Student.objects.get(admin=request.user.id)
    result=StudentResult.objects.filter(student_id=student)

    
    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark
        mark = assignment_mark + exam_mark
        print(i)
    context={
        'result':result,

        }
    return render(request,'Student/view_result.html',context)

def STUDENT_VIEW_NOTICE(request):

    student = Student.objects.get(admin=request.user.id)  
    courses = Course.objects.filter(name=student.course_id)
    notices = Notice.objects.filter(course__in=courses)
    
    context = {'notices': notices}
    print(notices)
    return render(request,'Student/view_notice.html',context)

def STUDENT_VIEW_ASSIGNMENT(request):
    student = request.user.student
    
    enrolled_course = student.course_id
    
    assignments = Assignment.objects.filter(subject_id__course=enrolled_course)
    
    student_submissions = Submission.objects.filter(student=request.user)
    print(student_submissions)
    # Create a list of tuples containing assignment ID and status
    assignment_status_list = []
    
    for assignment in assignments:
        submission = student_submissions.filter(assignment_id=assignment).first()
        status = submission.status if submission else 0
        assignment_status_list.append((assignment.id, status))
    
    context = {'assignments': assignments, 'assignment_status_list': assignment_status_list}
    
    return render(request, 'Student/view_assignment.html', context)

def STUDENT_COMPLETE_ASSIGNMENT(request,id):
    student = request.user.student
    assignment = Assignment.objects.get(id=id)
    subject = assignment.subject_id

    print(subject)

    context = {
        'student': student,
        'assignment': assignment,
        'subject': subject,
        }
    return render(request, 'Student/complete_assignment.html',context)

def STUDENT_SAVE_ASSIGNMENT(request):

    if request.method == 'POST':
        
        assignment_id = request.POST.get('assignment_id')  # Assuming you have a hidden input field for assignment_id in your form
        upload_file = request.FILES.get('upload_file')
        student = request.user
        assignment = Assignment.objects.get(id=assignment_id)
        subject = assignment.subject_id
        
        
        submission = Submission.objects.create(
            student=student,
            course=assignment.subject_id.course, 
            subject=subject,
            assignment=assignment,
            status=1,
            file=upload_file
        )
        
        assignment.save()
        messages.success(request,f'Assignment {assignment} is Successfully Completed !')
        
        return redirect('student_view_assignment')


