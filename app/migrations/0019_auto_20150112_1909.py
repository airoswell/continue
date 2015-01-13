# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20150109_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='zip_code',
            new_name='area',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='zip_code',
            new_name='primary_area',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='interested_areas',
            field=models.CharField(default=b'', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(default=b'', max_length=300, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='visibility',
            field=models.CharField(default=b'Private', max_length=10, choices=[(b'Private', b'Private'), (b'Ex-owners', b'Ex-owners'), (b'Public', b'Public')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemeditrecord',
            name='new_value',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemeditrecord',
            name='note',
            field=models.CharField(default=b'', max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemeditrecord',
            name='original_value',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2015, 2, 12)),
            preserve_default=True,
        ),
    ]
