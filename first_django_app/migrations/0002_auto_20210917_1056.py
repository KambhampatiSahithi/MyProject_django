# Generated by Django 3.2.7 on 2021-09-17 05:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_django_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userform',
            name='request_receive_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 10, 56, 15, 575671)),
        ),
        migrations.CreateModel(
            name='ResponseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=500)),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_django_app.userform')),
            ],
        ),
    ]
