from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('',views.home,name = 'home'),
    path('attendance',views.attendance,name = 'attendance'),
    path('student-information',views.show_students,name= 'student-information'),
    path('view-report',views.view_report,name = 'view-report'),
    path('search',views.search,name = 'search'),
    path('report',views.report,name ='report')
]