# Generated by Django 5.1.1 on 2024-10-24 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_dailyweathersummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='humidity',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weather',
            name='wind_speed',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='weather',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]