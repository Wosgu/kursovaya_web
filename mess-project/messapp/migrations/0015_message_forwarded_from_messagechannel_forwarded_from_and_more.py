# Generated by Django 5.0.3 on 2024-06-10 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messapp', '0014_delete_messageattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='forwarded_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messapp.message'),
        ),
        migrations.AddField(
            model_name='messagechannel',
            name='forwarded_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messapp.messagechannel'),
        ),
        migrations.AddField(
            model_name='messagegroup',
            name='forwarded_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messapp.messagegroup'),
        ),
    ]
