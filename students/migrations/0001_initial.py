# Generated by Django 3.0.5 on 2020-07-26 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applicants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th')], default='1st', max_length=3)),
                ('class_roll', models.CharField(default='00', max_length=5)),
                ('identity', models.CharField(max_length=50, unique=True)),
                ('roll', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('registration', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('applicant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='applicants.Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='StdLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
