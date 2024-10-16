from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Employer, JobSeeker


# ---------------------
# Формы для регистрации
# ---------------------


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин', 'autofocus': True})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'})
    )


class EmployerSignUpForm(UserCreationForm):
    company_name = forms.CharField(
        label="Наименование компании",
        widget=forms.TextInput(attrs={'placeholder': 'Введите наименование компании', 'class': 'form-control'})
    )
    inn = forms.CharField(
        label="ИНН",
        widget=forms.TextInput(attrs={'placeholder': 'Введите ИНН', 'class': 'form-control'})
    )
    industry = forms.CharField(
        label="Отрасль",
        widget=forms.TextInput(attrs={'placeholder': 'Введите отрасль', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'company_name', 'inn', 'industry', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите логин', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Введите пароль', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите пароль', 'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.USER_TYPE_CHOICES[0][0]
        if commit:
            user.save()
            Employer.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                inn=self.cleaned_data['inn'],
                industry=self.cleaned_data['industry'],
            )
        return user


class JobSeekerSignUpForm(UserCreationForm):

    full_name = forms.CharField(
        label="ФИО",
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше полное имя', 'class': 'form-control'})
    )
    education = forms.CharField(
        label="Ваше образование",
        widget=forms.TextInput(attrs={'placeholder': 'Уровень вашего образования', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'education', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите логин', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Введите пароль', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите пароль', 'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.USER_TYPE_CHOICES[1][0]
        if commit:
            user.save()
            JobSeeker.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                education=self.cleaned_data['education'],
            )
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
            'skills': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Ваши навыки'}),
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
