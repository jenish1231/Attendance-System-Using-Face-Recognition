from django.db import transaction
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)

            if request.user.is_superuser and request.user.is_authenticated:
                return redirect('admins:home')
            else:
                return redirect('teacher:home')

    form= AuthenticationForm()
    return render(request,'home.html',{'form':form})

def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


