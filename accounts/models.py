from django.db import models
from django.contrib.auth.models import User



gender_list = (('Male','Male'),('Female','Female'))
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,choices=gender_list)
    room = models.CharField(max_length=5)
    is_deleted = models.BooleanField(default=False)


