# Generated by Django 5.0.3 on 2024-04-22 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_alter_student_feedback_feedback_reply'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student_Feedback',
        ),
    ]
