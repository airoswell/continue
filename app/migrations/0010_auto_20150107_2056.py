# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_item_transferrable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='transferrable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
