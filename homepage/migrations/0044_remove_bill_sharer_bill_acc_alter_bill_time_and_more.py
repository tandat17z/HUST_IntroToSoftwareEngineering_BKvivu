# Generated by Django 4.2.4 on 2023-12-30 09:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0043_alter_bill_time_alter_post_time_alter_product_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='sharer',
        ),
        migrations.AddField(
            model_name='bill',
            name='acc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.account', verbose_name='Người mua'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 16, 46, 29, 556440)),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 16, 46, 29, 556440)),
        ),
        migrations.AlterField(
            model_name='product',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 16, 46, 29, 556440)),
        ),
    ]
