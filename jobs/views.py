import json

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import generics

from users.forms import EmployerSignUpForm

from .forms import JobForm
from .serializers import JobSerializer, ResponseSerializer, FeatureSerializer, SkillsSerializer
from .models import Feature, Skill, Job, Response as resp
from users.models import Review

# -------------------------------------
# Создание/удаление и просмотр вакансии
# -------------------------------------


def create_job(request):
    if request.user.is_authenticated and request.user.user_type == 'employer':
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.employer = request.user.employer_profile
                job.save()
                form.save_m2m()
                return redirect('home')
        else:
            form = JobForm()
        return render(request, 'jobs/job-creation.html', {'form': form})
  
    context = {
        'user_type': request.session.get('user_type'),
    }
    
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


def delete_job(request, job_id):
    if request.user.is_authenticated and request.user.user_type == 'employer':
        job = get_object_or_404(Job, id=job_id, employer=request.user.employer_profile)
        job.delete()
    return redirect('home')


def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    is_featured = Feature.objects.filter(job=job, user=request.user).first() if request.user.is_authenticated else False
    is_you = job.employer.user == request.user
    context = {
        'is_you':is_you,
        'job': job,
        'is_featured':is_featured,
        'skills': job.skills.all(),
        'user_type': request.session.get('user_type'),
    }
    
    reviews = Review.objects.filter(employer=job.employer)
    jobs = Job.objects.filter(employer=job.employer)
    
    context['employer'] = job.employer
    context['reviews'] = reviews
    context['reviews_count'] = reviews.count()
    context['jobs_count'] = jobs.count()

    if request.user.is_authenticated and request.user.user_type == 'seeker':
        context['responded'] = resp.objects.filter(job=job, job_seeker__user=request.user).first()

    return render(request, 'jobs/job-details.html', context)


# ------------------
# Отклик на вакансию
# ------------------


@login_required
def response_create_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    is_job_seeker = hasattr(request.user, 'jobseeker_profile')
    user_already_applied = False

    if is_job_seeker:
        user_already_applied = resp.objects.filter(job=job, job_seeker=request.user.jobseeker_profile).exists()

    if is_job_seeker:
        job_seeker_profile = request.user.jobseeker_profile
        if not user_already_applied:
            resp.objects.create(job=job, job_seeker=job_seeker_profile)
            job.resps += 1
            job.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def accept_resp(request, response_id):
    if request.user.user_type == 'employer':
        res = get_object_or_404(resp, id=response_id)
        if res.status == res.STATUS_CHOICES[0][0] and res.job.employer.user == request.user:
            res.status = res.STATUS_CHOICES[1][0]
            res.save()
        return redirect('responses_list_view')
    return redirect('home')


@login_required
def reject_resp(request, response_id):
    if request.user.user_type == 'employer':
        res = get_object_or_404(resp, id=response_id)
        if res.status == res.STATUS_CHOICES[0][0] and res.job.employer.user == request.user:
            res.status = res.STATUS_CHOICES[2][0]
            res.save()
        return redirect('responses_list_view')
    return redirect('home')


@login_required
def responses_list_view(request):
    if request.user.user_type == 'employer':
        resps = resp.objects.filter(job__employer=request.user.id)
        resps = resp.objects.filter(job__employer=request.user.id)
        return render(request, 'jobs/list-of-resps.html', {'resps': resps})
    return redirect('home')


@login_required
def my_resps_view(request):
    print(request.user.user_type)
    if request.user.user_type == 'seeker':
        resps = resp.objects.filter(job_seeker__user=request.user)
        return render(request, 'jobs/myresps.html', {'resps': resps})
    return redirect('home')

# ------------------
# Избранные вакансии
# ------------------


@login_required
def feature_create_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_featured = False

    if job and not already_featured:
        # print(request.user.id)
        Feature.objects.create(job=job, user=request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def feature_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    feature = get_object_or_404(Feature, job=job, user=request.user)
    feature.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def features_list_view(request):
    if request.user.is_authenticated:
        context = {
            'user_type': request.session.get('user_type'),
            'jobs' : [],
            'responded_jobs': [],
            'feature_jobs': [],
        }
        user_features = Feature.objects.filter(user=request.user)

        cities = user_features.values_list('job__location', flat=True).distinct()
        industries = user_features.values_list('job__industry', flat=True).distinct()
        context['cities'] = cities
        context['industries'] = industries

        if not user_features: 
            user_features = []

        if request.user.user_type == "seeker":
            user_responses = resp.objects.filter(job_seeker=request.user.jobseeker_profile) if hasattr(request.user, 'jobseeker_profile') else []
            responded_jobs = [response.job.id for response in user_responses]
            context['responded_jobs'] = responded_jobs

        featured_jobs = [feature.job.id for feature in user_features]
        context['featured_jobs'] = json.dumps(featured_jobs)

    return render(request, 'jobs/list-of-fts.html', context)


# -------------
# Views для API
# -------------


class JobDetail(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

@api_view(['GET'])
def all_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


class SkillsDetail(RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer

@api_view(['GET'])
def all_skills(request):
    skills = Skill.objects.all()
    serializer = SkillsSerializer(skills, many=True)
    return Response(serializer.data)


class ResponseDetail(RetrieveUpdateDestroyAPIView):
    queryset = resp.objects.all()
    serializer_class = ResponseSerializer

@api_view(['GET'])
def all_responses(request):
    jobs = resp.objects.all()
    serializer = ResponseSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def all_features(request, pk):
    jobs = Feature.objects.filter(user=pk)
    serializer = FeatureSerializer(jobs, many=True)
    return Response(serializer.data)


class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset

@api_view(['GET'])
def search_jobs(request):
    query = request.GET.get('q', '')
    industry = request.GET.get('industry', '')
    city = request.GET.get('city', '')

    jobs = Job.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(employer__company_name__icontains=query)
    )
    if industry:
        jobs = jobs.filter(industry__iexact=industry)
    if city:
        jobs = jobs.filter(location__iexact=city)

    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_features(request, pk):
    query = request.GET.get('q', '')
    industry = request.GET.get('industry', '')
    city = request.GET.get('city', '')

    jobs = Feature.objects.filter(user=pk)

    jobs = jobs.filter(
        Q(job__title__icontains=query) | Q(job__description__icontains=query) | Q(job__employer__company_name__icontains=query)
    )
    if industry:
        jobs = jobs.filter(job__industry__iexact=industry)
    if city:
        jobs = jobs.filter(job__location__iexact=city)

    serializer = FeatureSerializer(jobs, many=True)
    return Response(serializer.data)
