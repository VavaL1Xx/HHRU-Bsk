from django.shortcuts import render

# Create your views here.

from jobs.models import Job, Response, Feature

def home_view(request):
    jobs = Job.objects.all()
    
    context = {
        'jobs': jobs,
        'responded_jobs': [],
        'feature_jobs': [],
    }

    if request.user.is_authenticated:
        if request.user.user_type == "seeker":
            user_responses = Response.objects.filter(job_seeker=request.user.jobseeker_profile) if hasattr(request.user, 'jobseeker_profile') else []
            responded_jobs = [response.job.id for response in user_responses]
            context['responded_jobs'] = responded_jobs
        user_features = Feature.objects.filter(user=request.user.id)
        if not user_features: user_features = []
        featured_jobs = [feature.job.id for feature in user_features]
        context['featured_jobs'] = featured_jobs

    return render(request, 'users/home.html', context)