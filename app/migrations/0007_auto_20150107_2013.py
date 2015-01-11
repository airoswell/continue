# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150107_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtransactionrecord',
            name='post',
            field=models.ForeignKey(related_name='related_events', blank=True, to='app.Post', null=True),
            preserve_default=True,
        ),
    ]
