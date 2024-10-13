from rest_framework import serializers

from .models import Employer, JobSeeker, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employer
        fields = '__all__'

class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = JobSeeker
        fields = '__all__'

