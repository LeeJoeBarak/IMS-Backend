# Generated by Django 4.0.3 on 2022-05-07 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0005_rename_student_id_studentprofile_student_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompanyProfile',
        ),
    ]
