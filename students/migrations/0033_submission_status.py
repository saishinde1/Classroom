# Generated by Django 5.0.3 on 2024-04-29 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0032_alter_assignment_file_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
