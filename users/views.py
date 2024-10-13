from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from jobs.models import Job
from .forms import EmployerSignUpForm, JobSeekerSignUpForm, UserProfileForm, SeekerProfileForm, EmployerProfileForm
from .serializers import EmployerSerializer, JobSeekerSerializer, UserSerializer
from .models import JobSeeker, Employer, User


# -------------------------
# Регистрация и авторизация
# -------------------------


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


# ---------------
# Профиль и выход
# ---------------


@login_required
def profile_view(request):
    user = request.user

    user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user)
    seeker_form = SeekerProfileForm(request.POST or None, instance=user.jobseeker_profile) if hasattr(user, 'jobseeker_profile') else None
    employer_form = EmployerProfileForm(request.POST or None, instance=user.employer_profile) if hasattr(user, 'employer_profile') else None

    if request.method == 'POST':
        forms_valid = user_form.is_valid()
        if user.user_type == 'seeker' and seeker_form:
            forms_valid = forms_valid and seeker_form.is_valid()
        elif user.user_type == 'employer' and employer_form:
            forms_valid = forms_valid and employer_form.is_valid()

        if forms_valid:
            user_form.save()
            if seeker_form:
                seeker_form.save()
            if employer_form:
                employer_form.save()
            return redirect('profile')

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'seeker_form': seeker_form,
        'employer_form': employer_form,
    })


def logout_view(request):
    logout(request)
    return redirect('/')


# -------------
# Views для API
# -------------


class JobSeekerDetail(RetrieveUpdateDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer

@api_view(['GET'])
def all_seekers(request):
    seekers = JobSeeker.objects.all()
    serializer = JobSeekerSerializer(seekers, many=True)
    return Response(serializer.data)


class EmployerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

@api_view(['GET'])
def all_employers(request):
    employers = Employer.objects.all()
    serializer = EmployerSerializer(employers, many=True)
    return Response(serializer.data)


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
