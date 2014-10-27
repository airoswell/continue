# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_reguser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reguser',
            name='nickname',
            field=models.CharField(default=b'', max_length=140),
            preserve_default=True,
        ),
    ]
