# Generated by Django 4.0.2 on 2022-03-04 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0003_alter_hoursreport_date_alter_hoursreport_endtime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hoursreport',
            old_name='intern',
            new_name='internship',
        ),
    ]
