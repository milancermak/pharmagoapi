# Generated by Django 2.2.6 on 2021-04-18 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pharmagoapi.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=pharmagoapi.utils.now_with_tz)),
                ('updated_at', models.DateTimeField(default=pharmagoapi.utils.now_with_tz)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('created_at', models.DateTimeField(default=pharmagoapi.utils.now_with_tz)),
                ('updated_at', models.DateTimeField(default=pharmagoapi.utils.now_with_tz)),
                ('address', models.CharField(max_length=254)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=50)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pharmagoapi.Customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=pharmagoapi.utils.now_with_tz)),
                ('updated_at', models.DateTimeField(default=pharmagoapi.utils.now_with_tz)),
                ('medicine_name', models.CharField(blank=True, max_length=50, null=True)),
                ('medicine_description', models.CharField(blank=True, max_length=254, null=True)),
                ('dosage_description', models.CharField(blank=True, max_length=254, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmagoapi.Customer')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
