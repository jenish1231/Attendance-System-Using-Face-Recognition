from django.shortcuts import render,redirect
from .FR.Face import Train
from .models import Student,Attendance
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.db import connection
import cv2
import tkinter as tk
from tkinter import ttk
from django.contrib import messages


def home(request):

    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)

    total_student = Student.objects.filter(room=room[0]).count()

    report = Attendance.objects.select_related('student').filter(student__room=room[0],date=datetime.now().date())
    present_student = Attendance.objects.select_related('student').filter(student__room=room[0], date=datetime.now().date()).count()

    return render(request,'Teacher/index.html',{
        'present':present_student,
        'total_student':total_student,
        'report':report
    })

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def attendance(request):
    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    t = Train(room[0])
    label = t.showVideo()
    no_duplicates_list = set(label)
    not_of_class = set()

    current_user = request.user
    teacher = User.objects.get(username=current_user.username)
    for roll in no_duplicates_list:
        student = Student.objects.get(roll_no=roll)

        attended_student = Student.objects.filter(roll_no=roll,attendance__date=datetime.now().date())

        if attended_student.exists() :
            messages.warning(request, "Already took Attendance of the Student " + str(roll))
            pass
        else:
            a = Attendance()
            a.student = student
            a.teacher = teacher
            a.date = datetime.now()
            a.attended = True
            a.time = datetime.now().time()
            a.save()


    cv2.destroyAllWindows()

    return redirect('teacher:home')



def absent_student_information(request):
    present_student = Attendance.objects.select_related('student', 'teacher').filter(teacher=request.user,date=datetime.now().date()).count()

    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    total_student = Student.objects.filter(room=room[0]).count()

    report = Attendance.objects.select_related('student').filter(student__room=room[0], date=datetime.now().date())

    return render(request, 'Teacher/absent_student_information.html', {
        'students':report
    })

def show_students(request):
    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    students = Student.objects.all().filter(room=room[0])

    return render(request,'Teacher/show_students.html',{
        'students':students
    })

def create_date_range(date0='2018-01-01'):
    import datetime
    date1 = '2011-05-01'
    date2 = '2011-05-31'

    start = datetime.datetime.strptime(date1,'%Y-%m-%d')
    end = datetime.datetime.strptime(date2,'%Y-%m-%d')
    step = datetime.timedelta(days=1)
    dates = []
    while start <=end:
        dates.append(start.date())
        start+=step
    return dates

def view_report(request):

    mon = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12}
    months = {1: 'January', 2: 'Febuary', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    month =request.GET.get('mon')

    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    students = Student.objects.filter(room=room[0]).count()

    if month is None :
        month = 'Sept'

    c = connection.cursor()

    c.execute("select s.roll_no,sum(attended) "
              "from Teacher_attendance a inner join Teacher_student s "
              "where s.room = '{}' and a.student_id = s.id and "
              "date  between '2018-0{}-01' and '2018-0{}-31' "
              "group by a.student_id ".format(room[0], mon[month], mon[month]))

    row = c.fetchall()

    attendance_report = Attendance.objects.select_related('student').filter(date__month=mon[month])


    return render(request,'Teacher/view_report.html',{
        'months':mon,
        'report':attendance_report,
        'students':students,
        'row':row

    })

def search(request):

    s = request.GET.get('q')

    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)

    try:
        report = Attendance.objects.select_related('student').get(student__room=room[0],date=datetime.now().date(),student__roll_no=s)
    except:
        return JsonResponse({'error_message': 'Record not Found!!'})

    if report :
        student = {
            'status':True,
            'first_name':report.student.first_name,
            'last_name':report.student.last_name,
            'roll_no':report.student.roll_no,
            'attendance':'Present'
        }

        return JsonResponse(student)


def report(request):
    mon = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10,'Nov': 11, 'Dec': 12}
    month = request.GET.get('mon')
    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    attendance_report = Attendance.objects.select_related('student').filter(date__month=9,student__room=room[0]).values()
    student = Student.objects.all()
    c = Attendance.objects.select_related('student').filter(student__roll_no=5584).count()
    c = connection.cursor()
    c.execute('''select a.student_id,s.room  from Teacher_attendance a inner join Teacher_student s where s.room = '11A' and a.student_id = s.id and date  between '2018-09-01' and '2018-09-31' group by a.student_id ''')
    row = c.fetchall()
    print(room)
    attendance_report_list = list(attendance_report)
    return JsonResponse(attendance_report_list,safe=False)

