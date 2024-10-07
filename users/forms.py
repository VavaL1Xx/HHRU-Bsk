from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employer, JobSeeker

class EmployerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employer'
        if commit:
            user.save()
            Employer.objects.create(user=user, company_name=self.cleaned_data['company_name'])
        return user

class JobSeekerSignUpForm(UserCreationForm):
    resume = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'seeker'
        if commit:
            user.save()
            JobSeeker.objects.create(user=user, resume=self.cleaned_data['resume'])
        return user