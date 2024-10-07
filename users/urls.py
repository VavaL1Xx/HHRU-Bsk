from django.urls import path
from . import views

urlpatterns = [
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('signup/job_seeker/', views.job_seeker_signup, name='job_seeker_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.logout_view, name='profile'),
]