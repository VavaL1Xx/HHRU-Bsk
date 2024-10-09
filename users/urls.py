from django.urls import path
from . import views

urlpatterns = [
    path('api/user/', views.UserListCreate.as_view(), name='job-list'),
    path('api/user/<int:pk>', views.UserDetail.as_view(), name='job-list'),
    path('api/seek', views.JobSeekerListCreate.as_view(), name='job-list'),
    path('api/seek/<int:pk>/', views.JobSeekerDetail.as_view(), name='job-detail'),
    path('api/empl', views.EmployerListCreate.as_view(), name='job-list'),
    path('api/empl/<int:pk>/', views.EmployerDetail.as_view(), name='job-detail'),

    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('signup/job_seeker/', views.job_seeker_signup, name='job_seeker_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]