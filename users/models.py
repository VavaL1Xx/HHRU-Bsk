from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser

from manager.models import Skill


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Работодатель'),
        ('seeker', 'Соискатель'),
    )
    region = models.CharField(verbose_name='Регион', max_length=255, blank=True, null=True, default='')
    country = models.CharField(verbose_name='Страна',max_length=255, blank=True, null=True, default='')
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True, default='')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0][1])
    date_of_registration = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Фотография профиля")


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employer_profile')
    company_name = models.CharField(max_length=100, verbose_name="Наименование компании")
    inn = models.CharField(max_length=255, verbose_name="ИНН")
    industry = models.CharField(max_length=255, verbose_name="Отрасль")
    company_address = models.CharField(verbose_name='Адрес компании', max_length=255, blank=True, null=True)
    website = models.URLField(verbose_name='Сайт', blank=True, null=True)
    rating = models.FloatField(verbose_name="Рейтинг", default=.0)

    company_description = models.TextField(verbose_name="Описание компании", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.company_name}"


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='jobseeker_profile')
    full_name = models.CharField(verbose_name="ФИО", max_length=255)
    # skills = models.TextField(verbose_name="Навыки", blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='users', blank=False)
    education = models.CharField(max_length=255, verbose_name="Образование", blank=True, null=True)
    experience = models.TextField(verbose_name="Опыт работы", blank=True, null=True)
    
    desired_job_type = models.CharField(max_length=255, verbose_name="Желаемая категория работы", blank=True, null=True)
    desired_salary = models.CharField(max_length=50, verbose_name="Ожидаемая зарплата", blank=True, null=True)
    desired_location = models.CharField(max_length=100, verbose_name="Желаемое место работы", blank=True, null=True)
    
    portfolio_link = models.URLField(verbose_name="Ссылка на портфолио", blank=True, null=True)
    languages = models.TextField(verbose_name="Владеемые языки", blank=True, null=True)
    interests = models.TextField(verbose_name="Интересы", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"
    

class Review(models.Model):
    RATING_CHOICES = [
        (1, 'Отвратительно'),
        (2, 'Плохо'),
        (3, 'Средне'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='emp')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='us')
    date_of_creation = models.DateTimeField(verbose_name='Дата отзыва', auto_now_add=True)
    rate = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка')
    message = models.TextField(verbose_name="Отзыв", blank=True, null=True)


class Notification(models.Model):
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dest')
    message = models.TextField(verbose_name="Уведомление", blank=True, null=True)
    is_checked = models.BooleanField(verbose_name="Просмотрена", default=False)