# Generated by Django 5.1.6 on 2025-03-05 11:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_homwwork'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Homwwork',
            new_name='Homework',
        ),
    ]
