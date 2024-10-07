from django.shortcuts import render

# Create your views here.

from jobs.models import Job

def home_view(request):
    jobs = Job.objects.all()
    return render(request, 'users/home.html', {'jobs': jobs})