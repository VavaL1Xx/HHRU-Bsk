from django.db import models
from django.urls import reverse

# Create your models here.

from users.models import Employer, JobSeeker, User
from manager.models import Skill

class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('it', 'IT'),
        ('hr', 'HR'),
        ('finance', 'Финансы'),
        ('marketing', 'Маркетинг'),
        ('trade', 'Торговля'),
    )

    JOB_EMPLOYMENT_TYPE = (
        ('full', 'Полная занятость'),
        ('half', 'Неполная занятость'),
        ('free', 'Удаленно'),
    )

    title = models.CharField(verbose_name="Наименование вакансии", max_length=255)
    industry = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, verbose_name="Категория")
    employer = models.ForeignKey(Employer, verbose_name="Работодатель", on_delete=models.CASCADE, related_name='empl')
    skills = models.ManyToManyField(Skill, related_name='vacancies', blank=False)
    salary = models.CharField(verbose_name="Зарплата", max_length=255)

    work_exp = models.CharField(verbose_name="Опыт работы", max_length=32, blank=True, null=True)
    contact_email = models.EmailField(verbose_name="Контактный Email", blank=True)
    location = models.CharField(verbose_name="Место (Адрес)", max_length=255)
    description = models.TextField(verbose_name="Описание")
    
    employment_type = models.CharField(verbose_name="Тип занятости", choices=JOB_EMPLOYMENT_TYPE, max_length=50, default='full')
    resps = models.BigIntegerField(verbose_name="Кол-во откликов", default=0)
    date_of_creation = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f"[{self.employer.company_name}] {self.title}"

    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)])
    

class Response(models.Model):

    STATUS_CHOICES = [('pending', 'На рассмотрении'), ('accepted', 'Принят'), ('rejected', 'Отклонен')]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='responses')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='seeker')
    date_of_response = models.DateTimeField(verbose_name='Дата отклика', auto_now_add=True)
    
    cover_letter = models.TextField(verbose_name="Сопроводительное письмо", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    employer_feedback = models.TextField(verbose_name="Обратная связь", blank=True, null=True)

    class Meta:
        unique_together = ('job', 'job_seeker')

    def __str__(self):
        return f"{self.job_seeker.user.username} {self.job.title}"
    
    
class Feature(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='feature_job')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feature')
    
