# Generated by Django 4.0.3 on 2022-04-07 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0027_internshipandintern'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internshipandintern',
            old_name='inter',
            new_name='intern',
        ),
    ]
