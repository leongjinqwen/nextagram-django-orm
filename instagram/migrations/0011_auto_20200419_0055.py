# Generated by Django 3.0.5 on 2020-04-19 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0010_fanidol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.TextField(default='blank-profile-picture.png', max_length=255),
        ),
    ]
