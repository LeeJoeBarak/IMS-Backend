# Generated by Django 4.0.3 on 2022-04-07 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_student_status'),
        ('internship', '0026_alter_priority_status_decision_by_company_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipAndIntern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
                ('internship', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='internship.internshipdetails')),
            ],
        ),
    ]
