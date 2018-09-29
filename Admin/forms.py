from django import forms
from Teacher.models import Student
from django.conf import settings
from accounts.models import Teacher
from django.contrib.auth.models import User
import Teacher.choices as choices

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['room','gender']

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['first_name','last_name','roll_no','room','gender','image_path']
