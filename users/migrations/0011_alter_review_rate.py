# Generated by Django 5.1.1 on 2024-10-26 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_review_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(choices=[(1, 'Отвратительно'), (2, 'Плохо'), (3, 'Средне'), (4, 'Хорошо'), (5, 'Отлично')], verbose_name='Оценка'),
        ),
    ]
