# Generated by Django 4.0.2 on 2022-02-25 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(max_length=120)),
                ('programManager', models.CharField(max_length=120)),
                ('programCoordinator', models.CharField(max_length=120)),
                ('prioritiesAmount', models.PositiveIntegerField()),
                ('hoursRequired', models.PositiveIntegerField()),
            ],
        ),
    ]
