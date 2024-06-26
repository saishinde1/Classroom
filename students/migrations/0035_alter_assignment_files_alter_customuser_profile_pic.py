# Generated by Django 5.0.3 on 2024-04-30 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0034_rename_file_assignment_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='files',
            field=models.FileField(upload_to='assignments'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pic'),
        ),
    ]
