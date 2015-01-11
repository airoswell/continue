# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_userprofile_time_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-time_created']},
        ),
        migrations.AlterModelOptions(
            name='itemtransactionrecord',
            options={'ordering': ['-status', '-time_updated']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-time_posted']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-time_created']},
        ),
    ]
