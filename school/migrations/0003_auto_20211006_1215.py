# Generated by Django 3.2.7 on 2021-10-06 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_subjects_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='endterm',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(70), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='results',
            name='exam1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='results',
            name='exam2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterUniqueTogether(
            name='results',
            unique_together={('student', 'subjects')},
        ),
    ]
