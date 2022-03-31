# Generated by Django 4.0.3 on 2022-03-30 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_student_status'),
        ('program', '0014_programcoordinatorandprogram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companymentorandprogram',
            name='companyMentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.companymentor'),
        ),
        migrations.AlterField(
            model_name='programmanagerandprogram',
            name='programManager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.programmanager'),
        ),
    ]