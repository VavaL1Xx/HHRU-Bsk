# Generated by Django 5.1.1 on 2024-10-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование вакансии')),
                ('description', models.TextField(verbose_name='Описание')),
                ('location', models.CharField(max_length=255, verbose_name='Место (Адрес)')),
                ('salary', models.CharField(max_length=255, verbose_name='Зарплата')),
            ],
        ),
    ]