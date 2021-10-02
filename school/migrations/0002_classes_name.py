# Generated by Django 3.2.7 on 2021-10-02 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='name',
            field=models.CharField(choices=[('form one', 'form one'), ('form two', 'form two'), ('form three', 'form three'), ('form four', 'form four')], default='one', max_length=1000),
            preserve_default=False,
        ),
    ]
