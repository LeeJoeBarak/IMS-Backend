# Generated by Django 4.0.2 on 2022-03-04 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('program', '0004_alter_program_hoursrequired_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='programManager',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.programmanager'),
        ),
    ]