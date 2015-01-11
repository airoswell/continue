# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150105_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='visibility',
            field=models.CharField(default=b'Private', max_length=2, choices=[(b'Private', b'Private'), (b'ex-owners', b'ex-owners'), (b'Public', b'Public')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2015, 2, 6)),
            preserve_default=True,
        ),
    ]
