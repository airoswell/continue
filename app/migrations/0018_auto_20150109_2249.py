# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150109_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemeditrecord',
            name='original_value',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
