# Create your views here.

from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from jobs.models import Job
from .forms import EmployerSignUpForm, JobSeekerSignUpForm, UserProfileForm
from .serializers import EmployerSerializer, JobSeekerSerializer, UserSerializer
from .models import JobSeeker, Employer, User

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import generics


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


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

class JobSeekerListCreate(ListCreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer

class JobSeekerDetail(RetrieveUpdateDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer


@api_view(['GET'])
def all_seekers(request):
    # Получаем все вакансии
    jobs = JobSeeker.objects.all()
    serializer = JobSeekerSerializer(jobs, many=True)
    return Response(serializer.data)

class EmployerListCreate(ListCreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

class EmployerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


@api_view(['GET'])
def all_seekers(request):
    # Получаем все вакансии
    jobs = Employer.objects.all()
    serializer = EmployerSerializer(jobs, many=True)
    return Response(serializer.data)

class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def all_seekers(request):
    # Получаем все вакансии
    jobs = User.objects.all()
    serializer = UserSerializer(jobs, many=True)
    return Response(serializer.data)
