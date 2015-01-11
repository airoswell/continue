# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_item_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtransactionrecord',
            name='post',
        ),
    ]
