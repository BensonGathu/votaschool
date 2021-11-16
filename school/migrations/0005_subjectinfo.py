# Generated by Django 3.2.7 on 2021-11-16 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_report_all_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='subjectInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, null=True)),
                ('mean_marks', models.IntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subjects')),
            ],
            options={
                'unique_together': {('subject', 'student')},
            },
        ),
    ]
