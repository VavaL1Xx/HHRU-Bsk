from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employer, JobSeeker


class EmployerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'company_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employer'
        if commit:
            user.save()
            Employer.objects.create(user=user, company_name=self.cleaned_data['company_name'])
        return user


class JobSeekerSignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'seeker'
        if commit:
            user.save()
            JobSeeker.objects.create(user=user)
        return user
    

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите логин'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите электронную почту'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})