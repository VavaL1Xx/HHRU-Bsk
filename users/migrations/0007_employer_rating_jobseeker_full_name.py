# Generated by Django 5.1.1 on 2024-10-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_jobseeker_resume_employer_company_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='rating',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=5, verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='full_name',
            field=models.CharField(default=0, max_length=255, verbose_name='ФИО'),
            preserve_default=False,
        ),
    ]
