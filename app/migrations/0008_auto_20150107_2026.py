# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150107_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtransactionrecord',
            name='item',
            field=models.ForeignKey(related_name='transaction_records', to='app.Item'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtransactionrecord',
            name='post',
            field=models.ForeignKey(related_name='transaction_records', blank=True, to='app.Post', null=True),
            preserve_default=True,
        ),
    ]
