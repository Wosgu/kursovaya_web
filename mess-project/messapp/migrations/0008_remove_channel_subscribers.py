# Generated by Django 5.0.3 on 2024-06-08 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messapp', '0007_subscriberchannel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='subscribers',
        ),
    ]
