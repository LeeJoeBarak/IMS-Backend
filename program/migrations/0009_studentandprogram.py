# Generated by Django 4.0.2 on 2022-03-11 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_student_status'),
        ('program', '0008_alter_program_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAndProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.program')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
            ],
        ),
    ]
