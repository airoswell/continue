# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150108_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 8, 3, 17, 44, 862939), auto_now_add=True),
            preserve_default=False,
        ),
    ]
