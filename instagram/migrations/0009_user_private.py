# Generated by Django 3.0.5 on 2020-04-12 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0008_auto_20200412_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]