# Generated by Django 5.1.4 on 2025-01-13 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms_send', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smsconfiguration',
            old_name='name',
            new_name='username',
        ),
    ]