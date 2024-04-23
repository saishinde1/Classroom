from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from students.models import Course,Session_Year,CustomUser,Student,Teacher,Subject,Teacher_leave,Student_Feedback,Student_Leave,Attendance,Attendance_Report
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):
    user = request.session.get('user')
    return render(request, 'Student/home.html')

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

  
