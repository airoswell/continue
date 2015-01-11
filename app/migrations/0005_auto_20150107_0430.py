# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150106_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2015, 2, 7)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postanditemsrequest',
            name='message',
            field=models.ForeignKey(related_name='request', to='postman.Message'),
            preserve_default=True,
        ),
    ]
