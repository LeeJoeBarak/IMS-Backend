# Generated by Django 4.0.2 on 2022-02-25 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_student_cv_alter_student_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='cv',
        ),
        migrations.RemoveField(
            model_name='student',
            name='photo',
        ),
    ]
