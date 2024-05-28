# Generated by Django 3.2.12 on 2024-05-27 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.TextField(max_length=150, verbose_name='Name')),
                ('date', models.DateField(help_text='Date the event will take place.', verbose_name='Event Date')),
                ('time', models.TimeField(help_text='Time the event will take place.', verbose_name='Event Time')),
                ('place', models.TextField(max_length=250, verbose_name='Place')),
                ('file_cover', models.URLField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'db_table': 'event',
                'managed': True,
            },
        ),
    ]