# Generated by Django 3.2.7 on 2021-11-21 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20211121_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='class_teacher',
            field=models.ForeignKey(on_delete=models.SET('NoNe'), to='school.teacher'),
        ),
    ]
