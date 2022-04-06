from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import UserRegsiterForm
from ..filesys.models import Directory


def register_request(request):
    if request.method == 'POST':
        form = UserRegsiterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            root_dir = Directory(parent_dir=None,
                                 owner=request.user, abs_path='/')
            root_dir.save()
            return redirect('filesys:root')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    form = UserRegsiterForm()
    return render(request=request, template_name='users/register.html', context={'register_form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # todo: do sth with the below line...
                # messages.info(request, f'You are now logged in as {username}.')
                return redirect('filesys:root')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name='users/login.html', context={'login_form': form})


def logout_request(request):
    logout(request)
    return redirect("users:login")
