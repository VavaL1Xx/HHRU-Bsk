from django.urls import path
from . import views

urlpatterns = [
    path('create_job/', views.create_job, name='create_job'),
    path('view_job/<int:job_id>/', views.job_detail_view, name='job_detail_view'),
]