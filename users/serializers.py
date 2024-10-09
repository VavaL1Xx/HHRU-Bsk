from rest_framework import serializers

from .models import Employer, JobSeeker, User


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'