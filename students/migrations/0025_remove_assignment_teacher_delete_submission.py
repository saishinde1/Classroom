# Generated by Django 4.1.2 on 2024-04-23 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0024_assignment_submission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Submission',
        ),
    ]
