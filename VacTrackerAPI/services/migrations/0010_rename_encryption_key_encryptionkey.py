# Generated by Django 5.0.4 on 2024-05-15 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_alter_encryption_key_encryption_key'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='encryption_key',
            new_name='EncryptionKey',
        ),
    ]
