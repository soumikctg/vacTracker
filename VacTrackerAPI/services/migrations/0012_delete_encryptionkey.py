# Generated by Django 5.0.4 on 2024-05-16 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_alter_uservaccinedetails_vaccinator_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EncryptionKey',
        ),
    ]
