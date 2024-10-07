from django.db import models

# Create your models here.

from users.models import Employer

class Job(models.Model):
    employer = models.ForeignKey(Employer, verbose_name="Работодатель", on_delete=models.CASCADE, related_name='empl')
    title = models.CharField(verbose_name="Наименование вакансии", max_length=255)
    description = models.TextField(verbose_name="Описание")
    location = models.CharField(verbose_name="Место (Адрес)", max_length=255)
    salary = models.CharField(verbose_name="Зарплата", max_length=255)