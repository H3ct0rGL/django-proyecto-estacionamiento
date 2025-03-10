from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TasksForm
from .models import Tasks

# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html',{
            'form':UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user=User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{
                    'form':UserCreationForm,
                    'error':'Username already exists'
                })
        return render(request,'signup.html',{
            'form':UserCreationForm,
            'error':'Password do not match'
        })

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{
            'form':AuthenticationForm
        })
    else:
        user=authenticate(request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:            
            return render(request,'signin.html',{
                'form':AuthenticationForm,
                'error':'Username or password is incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')

def tasks(request):
    tasks=Tasks.objects.filter(user=request.user)
    return render(request,'tasks.html',{'tasks':tasks})

def create_tasks(request):
    if request.method=='GET':
        return render(request,'create_tasks.html',{
            'form':TasksForm,
        })
    else:
        try:
            form=TasksForm(request.POST)
            new_tasks=form.save(commit=False)
            new_tasks.user=request.user
            new_tasks.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_tasks.html',{
                'form':TasksForm,
                'error':'Please provide valida data'
            })
