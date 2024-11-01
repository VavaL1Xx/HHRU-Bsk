# Generated by Django 5.1.1 on 2024-10-26 07:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_jobseeker_skills_alter_user_user_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Уведомление')),
                ('destination', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dest', to=settings.AUTH_USER_MODEL)),
                ('source', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sour', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')),
                ('rate', models.CharField(choices=[('1', '1 - Очень плохо'), ('2', '2 - Плохо'), ('3', '3 - Средне'), ('4', '4 - Хорошо'), ('5', '5 - Отлично')], max_length=64, verbose_name='Оценка')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Отзыв')),
                ('employer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='emp', to='users.employer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='us', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
