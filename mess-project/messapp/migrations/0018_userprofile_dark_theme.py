# Generated by Django 5.0.6 on 2024-06-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messapp', '0017_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dark_theme',
            field=models.BooleanField(default=False),
        ),
    ]
