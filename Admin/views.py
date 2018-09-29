from django.shortcuts import render,redirect
from Teacher.models import Student,Attendance
from .forms import TeacherForm,StudentForm,UserForm
from django.contrib.auth.decorators import login_required
from accounts.models import Teacher
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import  csrf_exempt
from datetime import datetime
from django.db import connection
from Teacher.FR import Face
from django.contrib import messages

@login_required(login_url = '/accounts/login')
def home(request):
    teacher = User.objects.all().select_related('teacher')
    student = Student.objects.all()
    total_teacher = Teacher.objects.count()
    total_student = Student.objects.count()

    paginator = Paginator(student,6)
    page = request.GET.get('page',1)

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request,'Admin/index.html',{
        'teachers':teacher,
        'students':students,
        'totalTeacher':total_teacher,
        'totalStudent':total_student
    })

@login_required(login_url = '/accounts/login')
def editStudent(request,id):
    student = Student.objects.get(pk = id)

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            Student.objects.filter(id = id).update(
                first_name = form['first_name'].data,
                last_name = form['last_name'].data,
                gender = form['gender'].data,
                room = form['room'].data
            )

            return redirect('admins:home')

    form = StudentForm(instance=student)
    return render(request,'Admin/editStudent.html',{'form':form})

@login_required(login_url = '/accounts/login')
def deleteStudent(request,id):
    Student.objects.filter(id = id).delete()
    return redirect('admins:home')

@login_required(login_url = '/accounts/login')
def addTeacher(request):
    if request.method == "POST":
        teacher_form = TeacherForm(request.POST)
        user_form = UserForm(request.POST)
        if teacher_form.is_valid() and user_form:

            user = User.objects.create()
            first_name = user_form['first_name'].data
            last_name = user_form['last_name'].data
            email = user_form['email'].data
            username = user_form['username'].data
            password = user_form['password'].data

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.set_password(password)
            user.save()

            teacher = Teacher(
                user=user,
                room=teacher_form['room'].data,
                gender=teacher_form['gender'].data
            )

            teacher.save()

            return redirect('admins:home')

    teacher_form = TeacherForm()
    user_form = UserForm()

    return render(request,'Admin/addTeacher.html',{'user_form':user_form,'teacher_form':teacher_form})


#this baki
@login_required(login_url = '/accounts/login')
def editTeacher(request,id):
    teacher = Teacher.objects.get(pk=id)

    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():

            Teacher.objects.filter(id=id).update(
                first_name = form['first_name'].data,
                last_name = form['last_name'].data,
                gender = form['gender'].data,
                username = form['username'].data,
                password = form['password'].data
            )

            return redirect('admins:home')

    form = TeacherForm(instance=teacher)
    return render(request,'Admin/editTeacher.html',{'form':form})

def deleteTeacher(request,id):
    User.objects.filter(id = id).delete()
    return redirect('admins:home')

@login_required(login_url = '/accounts/login')
def addStudent(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid() :
            post_form = form.save(commit = False)
            post_form.save()

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('admins:home')
        return render(request,'Admin/addStudent.html',{'form':form,'error_message':'Invalid Submission'})
    form = StudentForm
    return render(request,'Admin/addStudent.html',{'form':form})

@csrf_exempt
def check_student_roll_no(request):
    roll = request.GET.get('roll_no')

    data = {
        'is_taken': Student.objects.filter(roll_no=roll).exists()
    }

    last_roll_no = Student.objects.latest('roll_no')

    if data['is_taken']:
        data['error_message'] = 'Student with ' + str(roll) + ' already exists!!\n Last Inserted Roll no : ' + str(last_roll_no)

    return JsonResponse(data)

@csrf_exempt
def check_image(request):
    path = request.GET.get('path')

    data = {
        'is_taken':Student.objects.filter(image_path=path).exists()
    }

    if data['is_taken']:
        data['error_message'] = 'Image Path Already Exists!!'

    return JsonResponse(data)


@csrf_exempt
def validate_image_path(request):
    path = request.GET.get('path')
    if path[7] is None:
        data = {
            'path_not_valid': True
        }
        if data['path_valid']:
            data['error_message'] = 'Image path not valid!!'
        return JsonResponse(data)
    return JsonResponse({'error_message':''})

@csrf_exempt
def validate_username(request):
    username = request.GET.get('username')
    data = {
        'is_taken' : User.objects.filter(username=username).exists()
    }

    if data['is_taken']:
        data['error_message'] = '{} already exists'.format(username)

    return JsonResponse(data)

@csrf_exempt
def validate_email(request):
    email = request.GET.get('email')
    data = {
        'is_taken' : User.objects.filter(email= email).exists()
    }

    if data['is_taken']:
        data['error_message'] = '{} already exists!!'.format(email)

    return JsonResponse(data)

def report(request):
    mon = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10,'Nov': 11, 'Dec': 12}
    months = {1:'January',2:'Febuary',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

    q_room = request.GET.get('search')
    q_month = request.GET.get('month')

    if q_room is None and q_month is None:
        q_room = '11A'
        q_month = 9


    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    report = Attendance.objects.select_related('student').filter(student__room=q_room, date=datetime.now().date())

    total_student = Student.objects.all().filter(room=q_room).count()
    c = connection.cursor()

    c.execute("select s.roll_no,sum(attended) "
              "from Teacher_attendance a inner join Teacher_student s "
              "where s.room = '{}' and a.student_id = s.id and "
              "date  between '2018-0{}-01' and '2018-0{}-31' "
              "group by a.student_id ".format(q_room,q_month,q_month))

    row = c.fetchall()

    return render(request,'Admin/view_report.html', {
        'report':report,
        'row':row,
        'months':mon,
        'total_student':total_student,
        'class':q_room,
        'date':months[int(q_month)]
    })


def train(request):
    room = User.objects.select_related('teacher').filter(username=request.user.username).values_list('teacher__room',flat=True)
    f = Face.Train(room[0])
    f.train_algorithm()
    messages.success(request,'Training Successfull')
    return redirect('admins:home')