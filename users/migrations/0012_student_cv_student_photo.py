# Generated by Django 4.0.2 on 2022-02-25 21:46

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_student_cv_remove_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cv',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='../media/'), upload_to='C:\\Users\\USER\\Desktop\\Yuval\\bgu\\backend\\ims_server\\cv', verbose_name='CV'),
        ),
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.FileField(blank=True, max_length=255, null=True, storage=django.core.files.storage.FileSystemStorage(location='../media/'), upload_to='C:\\Users\\USER\\Desktop\\Yuval\\bgu\\backend\\ims_server\\images', verbose_name='Profile Picture'),
        ),
    ]
