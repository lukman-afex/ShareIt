# Generated by Django 4.0.5 on 2022-09-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_userprofile_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_suspended',
        ),
        migrations.AddField(
            model_name='account',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
    ]
