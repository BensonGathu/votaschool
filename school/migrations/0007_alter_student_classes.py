# Generated by Django 3.2.7 on 2021-10-10 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20211010_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='classes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.classes'),
        ),
    ]
