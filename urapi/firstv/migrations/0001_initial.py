# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-15 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerName', models.CharField(max_length=50)),
                ('isTopRated', models.CharField(max_length=30)),
                ('fstmonthPostive', models.IntegerField()),
                ('fstmonthNetural', models.IntegerField()),
                ('fstMonthNegative', models.IntegerField()),
                ('sixMonthPostive', models.IntegerField()),
                ('sixMonthNetural', models.IntegerField()),
                ('sixMonthNegative', models.IntegerField()),
                ('tweMonthPostive', models.IntegerField()),
                ('tweMonthNetural', models.IntegerField()),
                ('tweMonthNegative', models.IntegerField()),
                ('createdDate', models.DateTimeField()),
            ],
        ),
    ]
