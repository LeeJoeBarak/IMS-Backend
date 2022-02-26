# Generated by Django 4.0.2 on 2022-02-25 20:57

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_student_cv_alter_student_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='cv',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='../media/cv'), upload_to='', verbose_name='CV'),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.FileField(blank=True, max_length=255, null=True, storage=django.core.files.storage.FileSystemStorage(location='../media/photos'), upload_to='', verbose_name='Profile Picture'),
        ),
    ]
