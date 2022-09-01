# Generated by Django 4.0.5 on 2022-08-31 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_alter_group_member_alter_group_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0004_rename_question_choice_poll'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'permissions': (('can_create_poll', 'Can create poll'),)},
        ),
        migrations.AddField(
            model_name='poll',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.group'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='poll_author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='poll',
            name='poll_text',
            field=models.CharField(max_length=200, null=True),
        ),
    ]