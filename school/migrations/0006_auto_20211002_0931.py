# Generated by Django 3.2.7 on 2021-10-02 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_auto_20211002_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='id',
            field=models.BigAutoField(auto_created=True, default='dd', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='results',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subjects'),
        ),
    ]
