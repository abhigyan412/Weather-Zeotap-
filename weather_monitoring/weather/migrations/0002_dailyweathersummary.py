# Generated by Django 5.1.1 on 2024-10-23 10:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyWeatherSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('avg_temperature', models.FloatField()),
                ('max_temperature', models.FloatField()),
                ('min_temperature', models.FloatField()),
                ('dominant_condition', models.CharField(max_length=100)),
            ],
            options={
                'unique_together': {('city', 'date')},
            },
        ),
    ]