# Generated by Django 3.2.7 on 2021-10-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='comments',
            field=models.CharField(default='commented', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='results',
            name='teacher',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
