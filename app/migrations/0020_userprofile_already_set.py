# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20150112_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='already_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
