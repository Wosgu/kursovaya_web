# Generated by Django 5.0.3 on 2024-06-11 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messapp', '0015_message_forwarded_from_messagechannel_forwarded_from_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='forwarded_from',
        ),
        migrations.RemoveField(
            model_name='messagechannel',
            name='forwarded_from',
        ),
        migrations.RemoveField(
            model_name='messagegroup',
            name='forwarded_from',
        ),
    ]
