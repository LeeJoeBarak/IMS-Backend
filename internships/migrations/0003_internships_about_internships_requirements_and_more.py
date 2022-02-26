# Generated by Django 4.0.2 on 2022-02-26 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0002_remove_internships_about_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='internships',
            name='about',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='internships',
            name='requirements',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='internships',
            name='internshipName',
            field=models.CharField(max_length=120, unique_for_year=True),
        ),
    ]
