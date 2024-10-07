from django.urls import path
from . import views

urlpatterns = [
    path('create_job/', views.create_job, name='create_job'),
]