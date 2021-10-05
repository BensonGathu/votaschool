# Generated by Django 3.2.7 on 2021-10-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='classes',
        ),
        migrations.AlterField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(related_name='students', to='school.Subjects'),
        ),
    ]
