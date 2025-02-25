from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import TasksForm
from .models import Tasks

# Create your views here.

# HOME
def home(request):
    return render(request,'home.html')

# SIGN UP
def signup(request):
    if request.method=='GET':
        return render(
            request,
            'signup.html',{
                'form':UserCreationForm
            }
        )
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
                return render(
                    request,
                    'signup.html',{
                        'form':UserCreationForm,
                        'error':'Username already exists'
                    }
                )
        return render(
            request,
            'signup.html',{
                'form':UserCreationForm,
                'error':'Password do not match'
            }
        )

# SIGN IN
def signin(request):
    if request.method=='GET':
        return render(
            request,
            'signin.html',{
                'form':AuthenticationForm
            }
        )
    else:
        user=authenticate(request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:            
            return render(
                request,
                'signin.html',{
                    'form':AuthenticationForm,
                    'error':'Username or password is incorrect'
                }
            )
        else:
            login(request,user)
            return redirect('tasks')

# SIGN OUT
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# TASKS
@login_required
def tasks(request):
    tasks=Tasks.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(
        request,
        'tasks.html',{
            'tasks':tasks
        }
    )
# TASKS COMPLETED
@login_required
def tasks_completed(request):
    tasks=Tasks.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(
        request,
        'tasks_completed.html',{
            'tasks':tasks
        }
    )
# TASKS DETAIL
@login_required
def tasks_detail(request,tasks_id):
    if request.method=='GET':
        tasks=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
        form=TasksForm(instance=tasks)
        return render(
            request,
            'tasks_detail.html',{
                'tasks':tasks,
                'form':form
            }
        )
    else:
        try:
            tasks=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
            form=TasksForm(request.POST,instance=tasks)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(
                request,
                'tasks_detail.html',{
                    'tasks':tasks,
                    'form':form,
                    'error':'Error updating task'
                }
            )
# CREATE TASKS
@login_required
def create_tasks(request):
    if request.method=='GET':
        return render(
            request,
            'create_tasks.html',{
                'form':TasksForm,
            }
        )
    else:
        try:
            form=TasksForm(request.POST)
            new_tasks=form.save(commit=False)
            new_tasks.user=request.user
            new_tasks.save()
            return redirect('tasks')
        except ValueError:
            return render(
                request,
                'create_tasks.html',{
                    'form':TasksForm,
                    'error':'Please provide valida data'
                }
            )
# COMPLETE TASKS
@login_required
def complete_tasks(request,tasks_id):
    tasks=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
    if request.method=='POST':
        tasks.datecompleted=timezone.now()
        tasks.save()
        return redirect('tasks')
# DELETE TASKS
@login_required
def delete_tasks(request,tasks_id):
    tasks=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
    if request.method=='POST':
        tasks.delete()
        return redirect('tasks')
