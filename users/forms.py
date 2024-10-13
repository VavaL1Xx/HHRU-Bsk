from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employer, JobSeeker


# ---------------------
# Формы для регистрации
# ---------------------


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
    

# -----------------
# Формы для профиля
# -----------------

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number', 'country', 'region', 'profile_picture',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль', 'type': 'password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта', 'type': 'email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш номер телефона', 'type': 'tel'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша страна'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш регион или город'}),
        }


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = [
            'education', 'experience', 'skills', 'desired_job_type', 'desired_salary',
            'desired_location', 'portfolio_link', 'languages', 'interests'
        ]
        widgets = {
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше образование'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш опыт работы'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваши навыки'}),
            'desired_job_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кем вы хотите работать'}),
            'desired_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваши зарплатные ожидания'}),
            'desired_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Желаемое место работы'}),
            'portfolio_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше портфолио', 'type': 'url'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Языки'}),
            'interests': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваши интересы'}),
        }


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = [
            'company_name', 'inn', 'industry', 'company_address', 'website', 'company_description'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компании'}),
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ИНН компании'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Чем занимается компания'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес компании'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Сайт компании', 'type': 'url'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание компании'}),
        }
