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
    # Add form validation to login/ signup pages too

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

    all_posts = PostData.objects.all() # Returns a list of post data objects(instance of a class which has functions/ variable)

    # print(type(all_posts))
    # <class 'django.db.models.query.QuerySet'>

    post_list = []
    
    for i in all_posts:
        post_dict = {}
        post_dict['title'] = i.Title
        post_dict['pk'] = i.pk
        post_dict['author'] = i.Author
        post_dict['category'] = i.Category
        post_dict['brief'] = i.Body[:250]
        post_dict['brief_required'] = len(i.Body)>250 
        # so if len(i.Body)>250 condition is true "len(i.Body)>250" is parsed as True
        post_dict['time'] = i.Time
        post_list.append(post_dict)

    return render(request, 'main/home.html',{"post_data_list": post_list})


@login_required
def post_detail(request, primary_key):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    try:
        current_post = PostData.objects.get(pk=primary_key)
    except:
        current_post = None



    # current_post = PostData.objects.filter(Category="Tech") -> Returns a list of objects
    # Exlore more around ,None in .get 
    # current_post = PostData.objects.get(pk=primary_key, None) -> returns one single object

    return render(request, 'main/post_detail.html', {"current_post": current_post})


@login_required
def new_post(request):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    # Add Form validation as a part of JS, to filter our invalid inputs

    current_user = request.user

    if request.method=='POST':
        print("PRINTING POST DATA ",request.POST)

        new_post = PostData.objects.create(Title=request.POST.get('title', None),
                                            Author=current_user,
                                            Category=request.POST.get('category', None),
                                            Body=request.POST.get('body', None)
                                            )
        
        return redirect(home)

    return render(request, 'main/new_post.html')


'''
Name
Email
Username
About
Age
Gender
'''