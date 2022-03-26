# Generated by Django 4.0.3 on 2022-03-25 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_student_status'),
        ('internship', '0020_delete_internship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoursreport',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.companymentor'),
        ),
        migrations.AlterField(
            model_name='hoursreport',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.student'),
        ),
    ]