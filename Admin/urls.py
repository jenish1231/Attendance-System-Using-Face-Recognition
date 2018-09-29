from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [

    path('',views.home,name = 'home'),
    path('addTeacher',views.addTeacher,name = 'add-teacher'),
    path('addStudent',views.addStudent,name = 'add-student'),
    path('teacher/<int:id>/edit',views.editTeacher,name= 'edit-teacher'),
    path('teacher/<int:id>/delete',views.deleteTeacher,name = 'delete-teacher'),
    path('student/<int:id>/edit',views.editStudent,name = 'edit-student'),
    path('student/<int:id>/delete',views.deleteStudent,name = 'delete-student'),
    path('check-roll',views.check_student_roll_no,name = 'check-roll'),
    path('validate-path',views.validate_image_path,name = 'validate-path'),
    path('validate-username',views.validate_username,name = 'validate-username'),
    path('validate-email',views.validate_email,name = 'validate-email'),
    path('report',views.report,name = 'report'),
    path('train',views.train,name = 'train'),
    path('check-image',views.check_image,name = 'check-image')

]