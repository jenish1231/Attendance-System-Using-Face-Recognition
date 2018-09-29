from django.db import models
from django.conf import settings
from datetime import datetime
from accounts.models import Teacher
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import choices

#value,text

path = settings.BASE_DIR + "/media/"

def check_roll(value):
    roll = Student.objects.filter(roll_no=value)

    if roll.exists():
        raise  ValidationError(_('%(value) already exists'),params={'value':value},)



class Student(models.Model):
    roll_no = models.IntegerField(unique=True,help_text='Roll No of the student')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20,choices=choices.gender_list)
    room = models.CharField(max_length=5,choices=choices.room_list)
    image_path = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    #image field

    def __str__(self):
        return str(self.roll_no)



class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    time = models.TimeField(blank = True)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return str(self.attended)