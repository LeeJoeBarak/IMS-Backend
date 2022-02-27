# Generated by Django 4.0.2 on 2022-02-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('program', models.CharField(max_length=120, primary_key=True, serialize=False, unique=True)),
                ('year', models.DateTimeField(auto_now=True)),
                ('semester', models.CharField(default='A', max_length=2)),
                ('prioritiesAmount', models.PositiveIntegerField()),
                ('hoursRequired', models.PositiveIntegerField()),
                ('department', models.CharField(default='Engine', max_length=100)),
            ],
        ),
    ]
