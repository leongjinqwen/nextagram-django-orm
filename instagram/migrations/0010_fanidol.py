# Generated by Django 3.0.5 on 2020-04-12 21:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0009_user_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='FanIdol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('approved', models.BooleanField(default=False)),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idols', to='instagram.User')),
                ('idol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fans', to='instagram.User')),
            ],
            options={
                'db_table': 'fanidol',
            },
        ),
    ]
