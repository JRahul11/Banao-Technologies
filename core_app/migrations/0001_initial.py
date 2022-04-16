# Generated by Django 3.2.12 on 2022-04-16 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Address',
                'db_table': 'Address',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_picture', models.ImageField(blank=True, default=None, upload_to='profilePictures')),
                ('email_id', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(blank=True, choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')], max_length=100, null=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User',
                'db_table': 'User',
            },
        ),
    ]
