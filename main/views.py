from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login_view(request):

    message = None

    if request.user.is_authenticated:
        return redirect(home)

    if request.method=='POST':
        print("PRINTING POST DATA ",request.POST)
        
        login_user = authenticate(request, username=request.POST['username'], password=request.POST['password'],) 

        if login_user:
            login(request, login_user)

            return redirect(home)
        else:
            message = "Wrong Credentials"

    return render(request, 'main/login.html',{'message': message})


@login_required
def home(request):
    return render(request, 'main/base.html')

