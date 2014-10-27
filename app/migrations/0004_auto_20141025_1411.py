# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_reguser_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.CharField(default=b'Gd', max_length=2, choices=[(b'nw', b'New'), (b'Ln', b'Like new'), (b'Gd', b'Good'), (b'Fl', b'Functional')]),
        ),
    ]
