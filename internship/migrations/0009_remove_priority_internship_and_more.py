# Generated by Django 4.0.2 on 2022-03-05 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0005_alter_program_programmanager'),
        ('internship', '0008_priority_internship_alter_internship_internshipname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='priority',
            name='internship',
        ),
        migrations.AlterField(
            model_name='internship',
            name='internshipName',
            field=models.CharField(max_length=120, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='internship',
            name='program',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='program.program'),
        ),
    ]