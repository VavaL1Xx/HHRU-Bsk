from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Работодатель'),
        ('seeker', 'Соискатель'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='seeker')
    date_of_registration = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Фотография профиля")

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employer_profile')
    company_name = models.CharField(max_length=100, verbose_name="Наименование компании")

    def __str__(self) -> str:
        return self.company_name

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user')
    resume = models.TextField(verbose_name="Резюме", null=True, blank=True)

    def __str__(self):
        return self.user.username