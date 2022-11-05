from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


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
    return render(request, 'todo/current.html')
