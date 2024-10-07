# Create your views here.

from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import EmployerSignUpForm, JobSeekerSignUpForm
from jobs.models import Job

def employer_signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            jobs = Job.objects.all()
            return render(request, 'users/home.html', {'jobs': jobs})
    else:
        form = EmployerSignUpForm()
    return render(request, 'users/register.html', {'form': form})


def job_seeker_signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            jobs = Job.objects.all()
            return render(request, 'users/home.html', {'jobs': jobs})
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                jobs = Job.objects.all()
                return render(request, 'users/home.html', {'jobs': jobs})
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    return redirect('/')