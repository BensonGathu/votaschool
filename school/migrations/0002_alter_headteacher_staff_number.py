# Generated by Django 3.2.7 on 2021-10-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headteacher',
            name='staff_number',
            field=models.CharField(max_length=2000),
        ),
    ]
