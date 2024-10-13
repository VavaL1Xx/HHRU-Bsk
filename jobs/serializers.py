from rest_framework import serializers

from .models import Job, Response, Feature
from users.serializers import EmployerSerializer, UserSerializer, JobSeekerSerializer

class JobSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    class Meta:
        model = Job
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    user = UserSerializer()
    class Meta:
        model = Feature
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    seeker = JobSeekerSerializer()
    job = JobSerializer()
    class Meta:
        model = Response
        fields = '__all__'
