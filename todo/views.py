from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})

    else:
        # Check if passwords are the same
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Create a new user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])

                # Commit to db
                user.save()

                # Login user
                login(request, user)

                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"User already exists"})

        else:
            # Tell the user that the passwords didn't match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Passwords didn't match, try again"})

def logoutuser(request):
    if request.method == 'POST':
        # Logout user
        logout(request)

        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})

    else:
        # Authenticate user
        user = authenticate(request, password=request.POST['password'], username=request.POST['username'])

        # If username/password don't match
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':"Username and password didn't match"})

        else:
            # Login user
            login(request, user)

            return redirect('currenttodos')

def home(request):
    return render(request, 'todo/home.html')

def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=True)

    return render(request, 'todo/current.html', {'todos':todos})

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})

    else:
        try:
            # Get data from form
            form = TodoForm(request.POST)

            # Save but don't commit to db
            new_todo = form.save(commit=False)

            # Add user to new todo
            new_todo.user = request.user

            # Commit to db
            new_todo.save()

            return redirect('currenttodos')

        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data sent in form, try again.'})

def viewtodo(request, todo_pk):
    # Get object
    todo = get_object_or_404(Todo, pk=todo_pk)

    if request.method == 'GET':
        # Create edit form
        form = TodoForm(instance=todo)

        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})

    else:
        try:
            # Get data from form
            form = TodoForm(request.POST, instance=todo)

            # Save object
            form.save()

            return redirect('currenttodos')

        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad data sent in form, try again.'})
