# Generated by Django 3.2.7 on 2021-11-15 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_report_s_mean_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='all_points',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
