from django.urls import path

from . import views

# URL для этих путей /jobs/...

urlpatterns = [
    
    # URL для API

    path('api/jobs/search/', views.search_jobs, name='search_jobs'),
    path('api/jobs/all/', views.all_jobs, name='all_jobs'),
    path('api/jobs/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),
    
    path('api/responses/all/', views.all_responses, name='all_responses'),
    path('api/responses/<int:pk>/', views.ResponseDetail.as_view(), name='response-detail'),
    
    path('api/features/all/', views.all_features, name='all_features'),
    path('api/features/<int:pk>/', views.FeatureDetail.as_view(), name='feature-detail'),
    
    # URL для Django

    path('responses/', views.responses_list_view, name='responses_list_view'),
    path('features/', views.features_list_view, name='features_list_view'),

    path('create/job/', views.create_job, name='create_job'),
    path('delete/job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('view/job/<int:job_id>/', views.job_detail_view, name='job_detail_view'),
    
    path('create/response/<int:job_id>/', views.response_create_view, name='job_response_view'),
    
    path('create/feature/<int:job_id>/', views.feature_create_view, name='job_feature_view'),
    path('delete/feature/<int:job_id>/', views.feature_delete, name='feature_delete_view'),
]