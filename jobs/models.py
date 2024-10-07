from django.db import models
from django.urls import reverse

# Create your models here.

from users.models import Employer

class Job(models.Model):
    employer = models.ForeignKey(Employer, verbose_name="Работодатель", on_delete=models.CASCADE, related_name='empl')
    title = models.CharField(verbose_name="Наименование вакансии", max_length=255)
    description = models.TextField(verbose_name="Описание")
    location = models.CharField(verbose_name="Место (Адрес)", max_length=255)
    salary = models.CharField(verbose_name="Зарплата", max_length=255)

    date_of_creation = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return "[" + str(self.employer) + "] " + self.title

    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)])