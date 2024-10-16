from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from jobs.models import Job
from .forms import EmployerSignUpForm, JobSeekerSignUpForm, UserProfileForm, SeekerProfileForm, EmployerProfileForm, UserLoginForm
from .serializers import EmployerSerializer, JobSeekerSerializer, UserSerializer
from .models import JobSeeker, Employer, User


# -------------------------
# Регистрация и авторизация
# -------------------------


def set_user_type(request, user_type):
    logout(request)
    request.session['user_type'] = user_type
    return redirect('home')


def employer_signup(request):
    context = {
        'user_type': request.session.get('user_type'),
    }
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = EmployerSignUpForm()

    context['form'] = form
    return render(request, 'users/register.html', context)


def job_seeker_signup(request):
    context = {
        'user_type': request.session.get('user_type'),
    }
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = JobSeekerSignUpForm()

    context['form'] = form
    return render(request, 'users/register.html', context)


def login_view(request):
    context = {
        'user_type': request.session.get('user_type'),
    }
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()

    context['form'] = form
    return render(request, 'users/login.html', context)


# ---------------
# Профиль и выход
# ---------------


@login_required
def profile_view(request):
    
    user = request.user
    user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user)
    seeker_form = SeekerProfileForm(request.POST or None, instance=user.jobseeker_profile) if hasattr(user, 'jobseeker_profile') else None
    employer_form = EmployerProfileForm(request.POST or None, instance=user.employer_profile) if hasattr(user, 'employer_profile') else None

    context = {
        'user_type': request.session.get('user_type'),
        'user_form': user_form,
        'seeker_form': seeker_form,
        'employer_form': employer_form,
    }

    if user.user_type == User.USER_TYPE_CHOICES[1][0]:
        context['skills'] = user.jobseeker_profile.skills.all()

    if request.method == 'POST':
        forms_valid = user_form.is_valid()
        if user.user_type == User.USER_TYPE_CHOICES[0][0] and seeker_form:
            forms_valid = forms_valid and seeker_form.is_valid()
        elif user.user_type == User.USER_TYPE_CHOICES[1][0] and employer_form:
            forms_valid = forms_valid and employer_form.is_valid()

        if forms_valid:
            user_form.save()
            if seeker_form:
                seeker_form.save()
            if employer_form:
                employer_form.save()
            return redirect('profile')

    return render(request, 'users/profile.html', context)


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
