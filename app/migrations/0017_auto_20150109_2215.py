# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_itemtransactionrecord_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2015, 2, 9)),
            preserve_default=True,
        ),
    ]
