# Generated by Django 5.1.1 on 2024-11-18 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WEB', '0002_rename_customuser_user2'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user2',
            new_name='CustomUser',
        ),
    ]
