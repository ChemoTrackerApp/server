# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-28 00:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patientprofile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patientprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='patientprofile',
            name='last_name',
        ),
    ]
