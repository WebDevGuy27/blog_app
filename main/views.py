from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        new_user = User.objects.create_user(username=request.POST.get('username',None), 
                                            email=request.POST.get('email',None), 
                                            password=request.POST.get('password',None),
                                            first_name=request.POST.get('name',None))
        new_user_data = UserData.objects.create(Gender=request.POST.get('gender',None),
                                                Age=request.POST.get('age',None),                                                
                                                About=request.POST.get('about',None),
                                                user_account = new_user
                                                )
        login(request, new_user)    

        return redirect(home)

    return render(request, 'main/signup.html')


def logout_view(request):
    logout(request)

    return redirect(home)

def home(request):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    all_posts = PostData.objects.all() # Returns a list of post data objects(instance of a class which has functions/ variable)

    # print(type(all_posts))
    # <class 'django.db.models.query.QuerySet'>

    post_list = []
    page_type = "home"
    
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

    return render(request, 'main/post_list.html',{"filtered_posts": post_list, "page_type": page_type})


def category_page(request, current_category):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    filtered_posts = PostData.objects.filter(Category=current_category) # Returns a list of post data objects(instance of a class which has functions/ variable)

    # print(type(all_posts))
    # <class 'django.db.models.query.QuerySet'>

    post_list = []

    page_type = "category"
    
    for i in filtered_posts:
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

    return render(request, 'main/post_list.html',{"filtered_posts": post_list, "page_type": page_type, "current_category": current_category})

@login_required
def my_posts(request):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    filtered_posts = PostData.objects.filter(Author=current_user) # Returns a list of post data objects(instance of a class which has functions/ variable)

    # print(type(all_posts))
    # <class 'django.db.models.query.QuerySet'>

    post_list = []

    page_type = "my_posts"
    
    for i in filtered_posts:
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

    return render(request, 'main/post_list.html',{"filtered_posts": post_list, "page_type": page_type})


@login_required
def edit_post(request, primary_key):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    try:
        current_post = PostData.objects.get(pk=primary_key)
    except:
        current_post = None

    # Verify if current user is the author of the current post

    message = None

    access_available = True

    if current_post:
        if current_user!=current_post.Author:
            access_available = False
    
    if request.method=='POST' and current_post:
        print("PRINTING SIGN UP POST DATA ",request.POST)

        current_post.Title = request.POST.get("title", None)
        current_post.Body = request.POST.get("body", None)
        current_post.Category = request.POST.get("category", None)
        current_post.save()

        message = "Your Edit has been saved successfully !"
        
        return render(request, 'main/edit_post.html', {"current_post": current_post, "access_value": access_available, "message": message})

    # current_post = PostData.objects.filter(Category="Tech") -> Returns a list of objects
    # Exlore more around ,None in .get 
    # current_post = PostData.objects.get(pk=primary_key, None) -> returns one single object

    return render(request, 'main/edit_post.html', {"current_post": current_post, "access_value": access_available, "message": message})

def post_detail(request, primary_key):
    # Django function to fetch the current user. Gives AnonymousUser/ Null as output if not logged in.
    current_user = request.user

    try:
        current_post = PostData.objects.get(pk=primary_key)
    except:
        current_post = None


    filtered_comments = CommentData.objects.filter(Post=current_post)

    if request.method=='GET':
        try:
            comment_page = request.GET.get('comment_page', 1)
            # print("PRINTING GET REQUEST DICTIONARY ",request.GET)
        except:
            comment_page = 1
    else:
        comment_page = 1    

    paginator = Paginator(filtered_comments, 3)

    try: 
        comment_data = paginator.page(comment_page)
    except:
        comment_data = paginator.page(1)

    logged_in = current_user.is_authenticated

    if request.method=='POST':
        new_comment = CommentData.objects.create(Comment=request.POST['comment'], Post=current_post)
        
        if logged_in:
            new_comment.Author = current_user
            new_comment.Name = current_user.first_name
            new_comment.Email = current_user.email
        elif request.POST['name']!='':
            new_comment.Name = request.POST['name']
            new_comment.Email = request.POST['email']


        new_comment.save()

        return redirect(post_detail, primary_key=primary_key)
            


    # current_post = PostData.objects.filter(Category="Tech") -> Returns a list of objects
    # Exlore more around ,None in .get 
    # current_post = PostData.objects.get(pk=primary_key, None) -> returns one single object

    return render(request, 'main/post_detail.html', {"current_post": current_post, "logged_in": logged_in, "comment_data": comment_data})



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