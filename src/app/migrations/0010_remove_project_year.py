# Generated by Django 3.2.13 on 2025-02-16 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='year',
        ),
    ]
