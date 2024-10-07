from django.shortcuts import get_object_or_404, render, redirect

from jobs.models import Job
from .forms import JobForm

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

def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job-details.html', {'job': job})
