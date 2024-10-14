import json

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import generics

from .forms import JobForm
from .serializers import JobSerializer, ResponseSerializer, FeatureSerializer
from .models import Feature, Job, Response as resp


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
                return redirect('home')
        else:
            form = JobForm()
        return render(request, 'jobs/job-creation.html', {'form': form})
    return redirect('home')

def delete_job(request, job_id):
    if request.user.is_authenticated and request.user.user_type == 'employer':
        job = get_object_or_404(Job, id=job_id, employer=request.user.employer_profile)
        job.delete()
    return redirect('home')

def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job-details.html', {'job': job})


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
            return redirect('home')
    return redirect('home')


@login_required
def responses_list_view(request):
    if request.user.user_type == 'employer':
        jobs = resp.objects.filter(job__employer=request.user.id)
        return render(request, 'jobs/list-of-resps.html', {'resps': jobs})
    return redirect('home')


# ------------------
# Избранные вакансии
# ------------------


@login_required
def feature_create_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_featured = False

    if job and not already_featured:
        print(request.user.id)
        Feature.objects.create(job=job, user=request.user)
        return redirect('home')
    return redirect('home')


@login_required
def feature_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    feature = get_object_or_404(Feature, job=job, user=request.user)
    feature.delete()
    return redirect('home')


@login_required
def features_list_view(request):
    context = {}
    user_features = Feature.objects.filter(user=request.user)
    if not user_features: 
        user_features = []

    featured_jobs = [feature.job.id for feature in user_features]
    context['featured_jobs'] = json.dumps(featured_jobs)
    print(featured_jobs)
    return render(request, 'jobs/list-of-fts.html', {'featured_jobs': featured_jobs})


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


class ResponseDetail(RetrieveUpdateDestroyAPIView):
    queryset = resp.objects.all()
    serializer_class = ResponseSerializer

@api_view(['GET'])
def all_responses(request):
    jobs = resp.objects.all()
    serializer = ResponseSerializer(jobs, many=True)
    return Response(serializer.data)


class FeatureDetail(RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

@api_view(['GET'])
def all_features(request):
    jobs = Feature.objects.all()
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
