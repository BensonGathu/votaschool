# Generated by Django 3.2.7 on 2021-12-13 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_auto_20211204_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='kcpe_marks',
            field=models.IntegerField(default=0),
        ),
    ]
