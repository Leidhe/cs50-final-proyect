from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def register(request):
    template = "users/register.html"
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    elif request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            
            if User.objects.filter(username=form.cleaned_data['username']).exists():                
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():                
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['firstname'],
                    last_name = form.cleaned_data['lastname'],
                    password = form.cleaned_data['password1']
                )
                user.save()
                
                # Login the user
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render(request, template, {'form': form})
    else:
        form = RegisterForm()
        return render(request, "users/register.html", {'form': form})

def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, "users/login.html", {'form': form, 'error_message': "Incorrect username or password. Please try again."})
    return render(request, "users/login.html", {'form': form})

def fun_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else: 
        return render(request, "orders/error.html", {'message': "An error has ocurred"})
