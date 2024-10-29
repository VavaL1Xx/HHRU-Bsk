from django.urls import path

from . import views

# URL для этих путей /users/...

urlpatterns = [
    
    # URL для API
    
    path('api/users/all/', views.all_users, name='users-list'),
    path('api/users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    
    path('api/seekers/all/', views.all_seekers, name='seekers-list'),
    path('api/seekers/<int:pk>/', views.JobSeekerDetail.as_view(), name='seeker-detail'),
    
    path('api/employers/all/', views.all_employers, name='employers-list'),
    path('api/employers/<int:pk>/', views.EmployerDetail.as_view(), name='employer-detail'),

    # URL для Django

    path('set_user_type/<str:user_type>/', views.set_user_type, name='set_user_type'),
    path('review/<int:pk>/', views.company_review, name='company_review'),
    
    path('view/company/<int:pk>/', views.company_profile, name='company_profile'),
    path('view/seeker/<int:pk>/', views.seeker_profile, name='seeker_profile'),

    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('signup/seeker/', views.job_seeker_signup, name='job_seeker_signup'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]