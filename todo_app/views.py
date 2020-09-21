from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo_app/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo_app/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'todo_app/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and Password did not match.'})
        else:
            login(request, user)
            return redirect('current_todos')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo_app/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo_app/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been chosen. Please pick another one.'})
        else:
            return render(request, 'todo_app/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_finished__isnull=True)
    return render(request, 'todo_app/current_todos.html', {'todos': todos})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo_app/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False) # does not put into the data base yet
            newtodo.user = request.user
            newtodo.save() # puts into the data base
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo_app/createtodo.html', {'form': TodoForm(), 'error': 'Bad data was passed in. Try again.'})

@login_required
def viewtodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance = todo)
        return render(request, 'todo_app/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo) # I'm overwriting the todo with the same id. This tells the data base not to make a new todo record.
            form.save() # puts into the data base
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo_app/viewtodo.html', {'todo': todo, 'form': form, 'error': "Bad data was passed in. Try again."})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.date_finished = timezone.now()
        todo.save()
        return redirect('current_todos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('current_todos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, date_finished__isnull=False).order_by('-date_finished')
    return render(request, 'todo_app/completed.html', {'todos': todos})
