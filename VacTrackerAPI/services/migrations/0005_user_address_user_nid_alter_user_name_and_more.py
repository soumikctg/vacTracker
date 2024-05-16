# Generated by Django 5.0.4 on 2024-05-15 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_vaccineinfo_uservaccinedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='Unknown', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='nid',
            field=models.CharField(default='Unknown', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='userId',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]