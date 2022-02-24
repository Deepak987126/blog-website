from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from rest_framework.generics import get_object_or_404

from .forms import SignUpForm, BlogForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django import http
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import BlogForm
from django.contrib.auth.models import User
from .models import MyBlog
from .forms import MyBlogForms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # for  pagination


# Create your views here.


def index(request):
    p = MyBlog.objects.all()
    p = Paginator(p, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    return render(request, 'app1/index.html', {'data': page_obj})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Successfully !!')
            form.save()
            return HttpResponseRedirect('/login/')

    else:
        form = SignUpForm()
    return render(request, 'app1/registeration.html', {'form': form})


# User login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'app1/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/profile/')


# Profile
@login_required()
def user_profile(request):
    if request.user.is_authenticated:
        all_blogs = MyBlog.objects.filter(author=request.user)
        # print(all_blogs)
        # print(reqeust.user.id)

    return render(request, 'app1/profile.html', {'name': request.user, 'allblogs': all_blogs})


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


# Change Password with old password
def user_change_pass(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/profile/')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, 'app1/change_password.html', {'form': fm, 'na'
                                                                     'me': request.user})


def task(request):
    return render(request, 'app1/task.html', )


def blog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                try:
                    messages.success(request, 'Your Registration has been successfully!!!')
                    form.save()
                    return redirect('/show')
                except:
                    pass
        else:
            form = BlogForm()
        return render(request, 'app1/blog.html', {'form': form})


def allrecord(request):
    record = User.objects.all()
    paginator = Paginator(record, 6)
    # print(paginator)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app1/allrecord.html', {'record': page_obj})


def myblog(request):
    if request.user.is_authenticated:
        # author= request.user.id
        # print(request.user)
        if request.method == "POST":
            fm = MyBlogForms(request.POST, request.FILES)
            if fm.is_valid():
                fm.instance.author = request.user
                messages.success(request, 'Post Uploaded Successfully!!!')
                fm.save()
                return redirect('profile')
        else:
            fm = MyBlogForms()

        return render(request, 'app1/myblog.html', {'form': fm})
    else:
        return redirect('login')


def search(request):
    item = request.POST.get('search_box')
    similar_blog = MyBlog.objects.filter(title=item)
    print(similar_blog)
    return render(request, 'app1/index.html', {'data': similar_blog})


def delete_post(request, id):
    if request.user.is_authenticated:
        user_posts = MyBlog.objects.filter(author=request.user, id=id)

        # print(user_posts,'?????')

        user_posts.delete()
        return redirect('/profile/')
    else:
        return redirect('login')


def view_single_post(request, id):
    if request.user.is_authenticated:
        single_post = MyBlog.objects.filter(id=id)
    else:
        single_post = MyBlog.objects.filter(id=id)
    return render(request, 'app1/Detailpost.html', {'post': single_post})


# def blog_search(request, search_box):
#     item= request.POST.get('search_box')
#     similar_blog=MyBlog.objects.filter(title=item)
#
#     return render(request, 'app/index.html', {'post':similar_blog})


def update_blog(request, id):
    instance = get_object_or_404(MyBlog, id=id)
    form = MyBlogForms(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'app1/myblog.html', {'form': form})


def update_profile(request, id):
     instance = User.objects.get(id=id)
     form = SignUpForm(request.POST or None, instance=instance)
     print(form)
     if form.is_valid():

        form.save()
        return redirect('profile')
     return render(request, 'app1/user_update_profile.html', {'form': form})

