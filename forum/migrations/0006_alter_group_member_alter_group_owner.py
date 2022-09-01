# Generated by Django 4.0.5 on 2022-08-31 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0005_comment_author_comment_likes_group_member_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='member',
            field=models.ManyToManyField(related_name='group_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to=settings.AUTH_USER_MODEL),
        ),
    ]
