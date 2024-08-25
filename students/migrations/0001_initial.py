# Generated by Django 5.0.1 on 2024-06-11 02:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_tools', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(default='studentavar.png', null=True, upload_to='students')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('admission_number', models.CharField(max_length=10, unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10)),
                ('registration_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('mobile', models.CharField(blank=True, max_length=13, null=True)),
                ('guardian', models.CharField(default='', max_length=100)),
                ('guardian_relation', models.CharField(choices=[('father', 'father'), ('mother', 'mother'), ('uncle', 'uncle')], default='Father', max_length=100)),
                ('guardian_mobile', models.CharField(blank=True, max_length=13, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('date_of_join', models.DateField(default='1998-01-01')),
                ('religion', models.CharField(max_length=20, null=True)),
                ('community', models.CharField(max_length=50, null=True)),
                ('address', models.TextField(null=True)),
                ('category', models.CharField(max_length=30, null=True)),
                ('feeconcession', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=False)),
                ('data_verified', models.BooleanField(default=False)),
                ('classroom', models.ManyToManyField(blank=True, to='admin_tools.classroom')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_tools.department')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['admission_number', 'department'],
            },
        ),
    ]
