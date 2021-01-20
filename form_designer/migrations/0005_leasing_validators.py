# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_designer', '0004_auto_20201026_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdefinitionfield',
            name='validators',
            field=models.IntegerField(blank=True, choices=[(0, 'EGN'), (1, 'EIK/BULSTAT')], null=True, verbose_name='Validators'),
        ),
    ]
