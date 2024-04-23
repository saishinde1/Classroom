# Generated by Django 5.0.3 on 2024-04-23 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0023_attendance_attendance_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_mark', models.IntegerField()),
                ('exam_mark', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.subject')),
            ],
        ),
    ]
