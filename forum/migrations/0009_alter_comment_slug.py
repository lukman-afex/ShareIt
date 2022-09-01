# Generated by Django 4.1 on 2022-09-01 01:06

import autoslug.fields
import builtins
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_reply_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=300, populate_from=builtins.id),
        ),
    ]