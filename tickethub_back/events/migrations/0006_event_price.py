# Generated by Django 4.2.11 on 2024-06-07 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20240605_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.BigIntegerField(default=10),
        ),
    ]
