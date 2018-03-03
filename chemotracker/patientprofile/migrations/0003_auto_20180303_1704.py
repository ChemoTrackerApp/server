# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-03 22:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patientprofile', '0002_auto_20180302_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='allergy',
        ),
        migrations.AddField(
            model_name='allergy',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientprofile.PatientProfile'),
        ),
    ]
