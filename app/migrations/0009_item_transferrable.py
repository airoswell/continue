# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150107_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='transferrable',
            field=models.IntegerField(default=1, max_length=1),
            preserve_default=True,
        ),
    ]
