# Generated by Django 4.2.7 on 2023-12-30 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0023_alter_bill_time_alter_post_provider_alter_post_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharer',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 17, 41, 18, 301707)),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 17, 41, 18, 302707)),
        ),
        migrations.AlterField(
            model_name='product',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 17, 41, 18, 301707)),
        ),
    ]
