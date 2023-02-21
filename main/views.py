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


def signup_view(request):

    if request.user.is_authenticated:
        return redirect(home)

    if request.method=='POST':
        print("PRINTING SIGN UP POST DATA ",request.POST)
        new_user = User.objects.create_user(username=request.POST.get('username',None), email=request.POST.get('email',None), password=request.POST.get('password',None))
        new_user_data = UserData.objects.create(Name=request.POST.get('name',None),
                                                Gender=request.POST.get('gender',None),
                                                Age=request.POST.get('age',None),
                                                Email=request.POST.get('email',None),
                                                About=request.POST.get('about',None),
                                                user_account = new_user
                                                )
        login(request, new_user)    

        return redirect(home)

    return render(request, 'main/signup.html')


def logout_view(request):
    logout(request)

    return redirect(home)

@login_required
def home(request):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    return render(request, 'main/base.html', {'username_value':current_user.username})


'''
Name
Email
Username
About
Age
Gender
'''