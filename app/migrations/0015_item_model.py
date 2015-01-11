# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_postitemstatus_item_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='model',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
