from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.JobListCreate.as_view(), name='job-list'),
    path('api/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),

    path('jobs/search/', views.search_jobs, name='search_jobs'),
    path('jobs/all/', views.all_jobs, name='all_jobs'),
    
    path('view_responses/', views.responses_list_view, name='responses_list_view'),
    path('view_features/', views.features_list_view, name='features_list_view'),

    path('create_job/', views.create_job, name='create_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('resp_job/<int:job_id>/', views.job_response_view, name='job_response_view'),
    path('feat_job/<int:job_id>/', views.job_feature_view, name='job_feature_view'),
    path('delfeat_job/<int:job_id>/', views.feature_delete, name='feature_delete_view'),
    path('view_job/<int:job_id>/', views.job_detail_view, name='job_detail_view'),
]