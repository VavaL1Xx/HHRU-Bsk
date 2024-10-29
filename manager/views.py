import json

from django.shortcuts import render

from jobs.models import Job, Response, Feature


# ------------------
# Домашняя страница
# ------------------


def home_view(request):
    jobs = Job.objects.all()
    cities = Job.objects.values_list('location', flat=True).distinct()
    industries = Job.objects.values_list('industry', flat=True).distinct()

    context = {
        'jobs': jobs,
        'responded_jobs': [],
        'feature_jobs': [],
    }

    if request.user.is_authenticated:
        context = {}
        if request.user.user_type == "seeker":
            user_responses = Response.objects.filter(job_seeker=request.user.jobseeker_profile) if hasattr(request.user, 'jobseeker_profile') else []
            responded_jobs = [response.job.id for response in user_responses]
            context['responded_jobs'] = responded_jobs
        
        user_features = Feature.objects.filter(user=request.user.id)
        
        if not user_features: 
            user_features = []
        
        featured_jobs = [feature.job.id for feature in user_features]
        
        context['featured_jobs'] = json.dumps(featured_jobs)
        
    context['cities'] = cities
    context['industries'] = industries
    context['user_type'] = request.session.get('user_type', 'seeker')

    return render(request, 'users/home.html', context)


def main_view(request):
    tp = request.session.get('user_type', 'seeker')
    context = {
        'user_type': tp,
    }
    
    if request.user.is_authenticated and request.user.user_type != tp:
        request.session['user_type'] = request.user.user_type

    return render(request, 'users/main.html', context)