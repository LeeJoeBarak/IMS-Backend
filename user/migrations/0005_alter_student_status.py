# Generated by Django 4.0.3 on 2022-03-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_systemmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(default='סטודנט', max_length=100),
        ),
    ]