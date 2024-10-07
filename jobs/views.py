from django.shortcuts import render, redirect
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